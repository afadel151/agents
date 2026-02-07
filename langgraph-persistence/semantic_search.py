from langgraph.store.memory import InMemoryStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import uuid

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)

store = InMemoryStore(
    index={
        "embed": embeddings,
        "dims": 768,
    }
)

user_id = "1"
namespace_for_memory = (user_id, "memories")



store.put(namespace_for_memory, str(uuid.uuid4()), {
        "food_preference": "I like pizza",
        "sport_preference": "basketball"
    },
    index=["food_preference","sport_preference"]
)
store.put(namespace_for_memory,str(uuid.uuid4()),{
        "phone": "iPhone",
        "car_preference": "mercedes"
    },
    index=["phone"]    
)
results = store.search(
    namespace_for_memory,
    query="What phone does the user have?",
    limit=1
)

print(results[0].value)


## we can acess memory at any node :

# def update_memory(state: MessagesState, config: RunnableConfig, *, store: BaseStore):

#     # Get the user id from the config
#     user_id = config["configurable"]["user_id"]

#     # Namespace the memory
#     namespace = (user_id, "memories")

#     # ... Analyze conversation and create a new memory
    
#     # Create a new memory ID
#     memory_id = str(uuid.uuid4())

#     # We create a new memory
#     store.put(namespace, memory_id, {"memory": memory})