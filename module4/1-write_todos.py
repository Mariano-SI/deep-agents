from langchain.agents.middleware import TodoListMiddleware
from deepagents import create_deep_agent

agent = create_deep_agent(
    tools=[...],
    middleware=[TodoListMiddleware()],
)