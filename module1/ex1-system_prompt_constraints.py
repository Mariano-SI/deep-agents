from deepagents import create_deep_agent
from models import model

SYSTEM_PROMPT = """
Você é um especialista em matematica que responde questoes matematicas feitas pelo usuário. Qualquer pergunta enviada pelo usuário fora do escopo matematico vocew deve explicitamente responder que não é capaz de lhe auxiliar em questoes que além da matematica.
"""

math_agent = create_deep_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    name="math_agent"
)
question = input("Envie uma questao ao agent: ")

response = math_agent.invoke({"messages":[{"role":"user", "content": question}]})

print(response["messages"][-1].content)