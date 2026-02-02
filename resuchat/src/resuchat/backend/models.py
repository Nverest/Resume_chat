from pydantic import BaseModel, Field
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector
from dotenv import load_dotenv

load_dotenv()
embedding_model = get_registry().get("gemini-text").create(name="gemini-embedding-001")

EMBEDDING_DIM = 3072

class Resume(LanceModel):
    doc_id: str 
    filepath: str
    filename: str = Field(description="name of the file")
    content: str = embedding_model.SourceField()
    embedding: Vector(EMBEDDING_DIM) = embedding_model.VectorField()

class ResumeSection(BaseModel):
    jobs: list[str] = Field(description="list of name of jobs")
    internships: list[str] = Field(description="list of name of internships")
    education: list[str]= Field(description="list of name of schools and courses")
    projects: list[str]=Field(description="list of projects and brief description of them")
    skills: list[str]=Field(description="list of skills")

class Prompt(BaseModel):
    prompt: str = Field(description="prompt from user, if empty consider prompt as missing")

class ChatResponse(BaseModel):
    answer: str = Field(description="answer based on the prompt and context")