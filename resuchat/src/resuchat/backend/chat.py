from pydantic_ai import Agent
from models import ChatResponse, ResumeSection
from constants import VECTOR_DATABASE_PATH
import lancedb

chat_agent = Agent(
    model="google-gla:gemini-2.5-flash",
    retries=3,
    system_prompt=(
        "You are a impersonator bot that impersonates the person based on the "
        "provided resume and coverletters, you will answer questions as if you "
        "are that person, try to make a persona based on the information. Always use the retrieve_top_documents tool before "
        "answering any question. Do not hallucinate any information. If the "
        "information is not present in the provided documents, respond with 'I do not know' or equivalent in prompted language "
        "always retrive documents before answering"
        "you have access to previus chat messages"
    ),
    output_type=ChatResponse,
)

extract_agent = Agent(
    model="google-gla:gemini-2.5-flash",
    retries=3,
    system_prompt=(
        "Extract structured sections from the provided resume text. "
        "Return job titles with company names, internships with company names education entries, "
        "project names, and key skills. "
    ),
    output_type=ResumeSection
)


@chat_agent.tool_plain
def retrieve_top_documents(query: str, k=3) -> str:
    """
    Uses vector search to find the closest k matching documents to the query
    """
    try:
        db = lancedb.connect(uri=VECTOR_DATABASE_PATH)
        if "Resume" not in db.table_names():
            return "No matching documents found"
        results = db["Resume"].search(query=query).limit(k).to_list()
        if not results:
            return "No data"

        return "\n\n".join(
            f"filename: {doc['filename']}\nContent: {doc['content']}" for doc in results
        )
    except Exception as e:
        return f"Error retrieving documents: {str(e)}"