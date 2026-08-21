import os  # noqa: F401  # used in commented-out model examples below
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env", override=True)

from langchain.chat_models import init_chat_model

# Anthropic models
model = init_chat_model("anthropic:claude-haiku-4-5", timeout=60, max_retries=2)
strong_model = init_chat_model("anthropic:claude-sonnet-4-6", timeout=120, max_retries=2)

# OpenAI models
model = init_chat_model("openai:gpt-4.1-mini")
strong_model = init_chat_model("openai:gpt-4.1")
