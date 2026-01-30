from pydantic_ai import Agent
from models import ChatResponse
from constants import VECTOR_DATABASE_PATH
import lancedb

vector_db = lancedb.connect(uri=VECTOR_DATABASE_PATH)

chat_agent = Agent(
    model="google-gla:gemini-2.5-flash",
    retries=3,
    system_prompt=(
        "You are a impersonator bot that impersonates the person based on the "
        "provided resume and coverletters, you will answer questions as if you "
        "are that person. Always use the retrieve_top_documents tool before "
        "answering any question. Do not hallucinate any information. If the "
        "information is not present in the provided documents, respond with 'I do not know' or equivalent in prompted language"
    ),
    output_type=ChatResponse,
)


@chat_agent.tool_plain
def retrieve_top_documents(query: str, k=3) -> str:
    """
    Uses vector search to find the closest k matching documents to the query
    """
    results = vector_db["Resume"].search(query=query).limit(k).to_list()

    return "\n\n".join(
        f"filename: {doc['filename']}\nContent: {doc['content']}" for doc in results
    )
