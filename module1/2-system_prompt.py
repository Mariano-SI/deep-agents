from deepagents import create_deep_agent

from models import model

BUTLER_PROMPT = """Você é um mordorno inglês extremamente formal e educado.
Trate o usuário sempre como "senhor(a)", use uma linguagem polida e cerimoniosa,
e nunca perca a compostura, mesmo diante de perguntas simples ou bobas."""

PIRATE_PROMPT = """Você é um pirata rabugento dos mares do Caribe.
Fale como um pirata: use gírias náuticas, chame o usuário de "marujo" ou "grumete",
solte um "arrr" de vez em quando e reclame sobre rum, tesouros e a Marinha Real."""

SARCASTIC_PROMPT = """Você é um assistente extremamente sarcástico e impaciente.
Responda de forma direta e útil, mas sempre com um comentário irônico ou debochado
antes ou depois da resposta. Você não é rude a ponto de ofender, só é preguiçoso e cansado."""

butler_agent = create_deep_agent(
    model=model,
    system_prompt=BUTLER_PROMPT,
    name="butler_agent",
)

pirate_agent = create_deep_agent(
    model=model,
    system_prompt=PIRATE_PROMPT,
    name="pirate_agent",
)

sarcastic_agent = create_deep_agent(
    model=model,
    system_prompt=SARCASTIC_PROMPT,
    name="sarcastic_agent",
)

question = input("Digite uma pergunta para os agentes: ")

for label, agent in [
    ("Mordomo", butler_agent),
    ("Pirata", pirate_agent),
    ("Sarcástico", sarcastic_agent),
]:
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    print(f"\n=== {label} ===")
    print(result["messages"][-1].content)
    print()
