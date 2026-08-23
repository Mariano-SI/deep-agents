import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
from pathlib import Path

import requests
from deepagents import create_deep_agent
from langchain_community.utilities import SQLDatabase
from langchain_core.tools import tool

from models import model

DB_PATH = Path(__file__).parent / "chinook.db"
db = SQLDatabase.from_uri(f"sqlite:///{DB_PATH}")

SYSTEM_PROMPT = """You are a SQL analyst with access to the Chinook music store database.

Rules:
- Use read_sql for SELECT queries.
- Do not modify the database.
- If a tool returns an error, revise the SQL and try again.
- Show your SQL in your final answer.
"""


@tool
def read_sql(query: str) -> str:
    """Run a read-only SELECT query against the Chinook music store database."""
    try:
        return str(db.run(query))
    except Exception as e:
        return f"Error: {e}"


sql_agent = create_deep_agent(
    model=model,
    name="SQL_Agent",
    tools=[read_sql],
    system_prompt=SYSTEM_PROMPT,
)

result = sql_agent.invoke(
    {"messages": [{"role": "user", "content": "Which five genres have the most tracks?"}]}
)

for message in result["messages"]:
    message.pretty_print()


COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"

CRYPTO_SYSTEM_PROMPT = """You are a cryptocurrency market assistant with access to live data from CoinGecko.

Rules:
- get_crypto_price needs a CoinGecko coin id (lowercase, e.g. "bitcoin", "ethereum",
  "solana"), not a ticker symbol like "BTC".
- If you don't know a coin's id, call search_crypto_coin first to resolve it.
- If a tool returns an error, adjust the input and try again.
- State the currency clearly in your final answer.
"""


@tool
def search_crypto_coin(query: str) -> str:
    """Search CoinGecko for coins matching a name or ticker (e.g. "BTC", "sol").

    Returns up to 5 matches with their CoinGecko id, name and symbol. Use the id
    with get_crypto_price.
    """
    try:
        response = requests.get(
            f"{COINGECKO_BASE_URL}/search",
            params={"query": query},
            timeout=10,
        )
        response.raise_for_status()
        coins = response.json().get("coins", [])[:5]
        if not coins:
            return f"No coins found for '{query}'."
        return "\n".join(f"{c['id']} — {c['name']} ({c['symbol'].upper()})" for c in coins)
    except Exception as e:
        return f"Error: {e}"


@tool
def get_crypto_price(coin_id: str, vs_currency: str = "usd") -> str:
    """Get the current price of a cryptocurrency from CoinGecko.

    Args:
        coin_id: CoinGecko coin id, e.g. "bitcoin", "ethereum", "solana".
        vs_currency: Currency to price against, e.g. "usd", "brl", "eur".
    """
    try:
        response = requests.get(
            f"{COINGECKO_BASE_URL}/simple/price",
            params={
                "ids": coin_id,
                "vs_currencies": vs_currency,
                "include_24hr_change": "true",
                "include_last_updated_at": "true",
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        if coin_id not in data:
            return f"Coin id '{coin_id}' not found. Try search_crypto_coin first."
        return str(data[coin_id])
    except Exception as e:
        return f"Error: {e}"


crypto_agent = create_deep_agent(
    model=model,
    name="Crypto_Agent",
    tools=[search_crypto_coin, get_crypto_price],
    system_prompt=CRYPTO_SYSTEM_PROMPT,
)

crypto_result = crypto_agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What is the current price of Bitcoin, Ethereum and Solana in USD?",
            }
        ]
    }
)

for message in crypto_result["messages"]:
    message.pretty_print()


