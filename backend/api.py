from fastapi import FastAPI
from backend.app.chat import chat_agent
from backend.app.models import Prompt, ResumeSumarizerInput

app = FastAPI()

# Create a single Chat instance to maintain conversation history
@app.post("/chat/resume")
async def query_doc(query: ResumeSumarizerInput):
    result = await chat_agent.run(query.prompt)
    return result.output

@app.post("/chat/query")
async def query_doc(query: Prompt):
    result = await chat_agent.run(query.prompt)
    
    return result.output