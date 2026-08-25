# python/m2/m2.4_interpreter_agent.py
from pprint import pprint

from langchain_quickjs import CodeInterpreterMiddleware
from deepagents import create_deep_agent
from models import model

SYSTEM_PROMPT= """
Voce é um especialista em matematica e reposte perguntas matematicas de forma clara. Se o input dado por algo sem relacao as consultas matematicas deixe explicito que ovce nao é capaz de ajudar. PRecisa relizar calculos atraves de scripts que pensar sobre eles
"""

agent = create_deep_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    middleware=[CodeInterpreterMiddleware()],
)


result = agent.invoke({"messages":[{"role":"user", "content":"Quanto é: (37² − 15) × 4 ÷ 2 + √225 − 8³ ÷ 16"}]})

for message in result["messages"]:
    print("=" * 80)
    print(f"[{message.__class__.__name__}]")
    print("=" * 80)
    pprint(message)
    print()

