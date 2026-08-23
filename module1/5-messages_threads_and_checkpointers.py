from deepagents import create_deep_agent
from langgraph.checkpoint.memory import MemorySaver


from models import model

agent = create_deep_agent(
    model=model,
    checkpointer=MemorySaver()
)

thread_a = {"configurable": {"thread_id": "thread-a"}}
thread_b = {"configurable": {"thread_id": "thread-b"}}


#Using thread A
result = agent.invoke(
    {"messages": [{"role": "user", "content": "Remember that my favorite colour is blue."}]},
    config=thread_a,
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What is my favorite colour?"}]},
    config=thread_a,
)

print("Thread A response")
print(result["messages"][-1].content)
print()

# Using thread B

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What is my favorite colour?"}]},
    config=thread_b,
)

print("Thread B response")
print(result["messages"][-1].content)
print()



