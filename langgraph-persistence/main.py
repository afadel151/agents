
# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
# load_dotenv()



# model = ChatGoogleGenerativeAI(
#     model="gemini-2.0-flash",
# )

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables import RunnableConfig
from typing import Annotated
from typing_extensions import TypedDict
from operator import add

class State(TypedDict):
    foo: str
    bar: Annotated[list[str], add]

def node_a(state: State):
    return {"foo": "a", "bar": ["a"]}

def node_b(state: State):
    return {"foo": "b", "bar": ["b"]}


workflow = StateGraph(State)
workflow.add_node(node_a)
workflow.add_node(node_b)
workflow.add_edge(START, "node_a")
workflow.add_edge("node_a", "node_b")
workflow.add_edge("node_b", END)

checkpointer = InMemorySaver()
graph = workflow.compile(checkpointer=checkpointer)

config: RunnableConfig = {"configurable": {"thread_id": "1"}}
graph.invoke({"foo": "", "bar":[]}, config)



# checkpoints = list(checkpointer.list(config))

# for i, cp in enumerate(checkpoints):
#     print(f"\n###Checkpoint {i}")
#     print("Config:", cp.config)
#     print("Version seen:", cp.checkpoint['versions_seen'])
#     print("Channel values:", cp.checkpoint['channel_values'])
#     print("Updated channels:", cp.checkpoint['updated_channels'])
#     # print("\nChannel Version:", cp.channel_versions)



snapshot = graph.get_state(config)

# print(snapshot.values)

history = graph.get_state_history(config)

for h in history:
    print(h.values)