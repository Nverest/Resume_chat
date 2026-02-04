from fastapi import FastAPI, UploadFile, File
from chat import chat_agent, extract_agent
from models import Prompt, Resume
from constants import VECTOR_DATABASE_PATH
from pypdf import PdfReader
import lancedb
import io

app = FastAPI()

@app.post("/chat/query")
async def query_doc(query: Prompt):
    result = await chat_agent.run(query.prompt)
    return result.output

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload and process resume/cover letter files"""
    try:
        content = await file.read()

        if file.filename.endswith('.pdf'):
            pdf_reader = PdfReader(io.BytesIO(content))
            text = "".join(page.extract_text() +"\n" for page in pdf_reader.pages)
        else:
            text = content.decode('utf-8')

        # only save to vector
        db = lancedb.connect(uri=VECTOR_DATABASE_PATH)
        if "Resume" in db.table_names():
            db.drop_table("Resume")
        table = db.create_table("Resume", schema=Resume)
        # Ingest into vector database
        db = lancedb.connect(uri=VECTOR_DATABASE_PATH)
        
        doc_id = file.filename.split('.')[0].lower()

        # Add new entry
        table.add([
            {
                "doc_id": doc_id,
                "filepath": str(file.filename),
                "filename": doc_id,
                "content": text
            }
        ])
        
        return {"status": "success", "filename": file.filename}
    except Exception as e:
        import traceback
        return {"status": "error", "message": str(e), "trace": traceback.format_exc()}
    
@app.get("/resume/sections")
async def get_resume_sections():
    vector_db = lancedb.connect(uri=VECTOR_DATABASE_PATH)
    """extract structured sections from latest uploaded resume"""
    results = vector_db["Resume"].search("resume internships education projects skills").limit(5).to_list()

    all_content = "\n\n".join(doc["content"] for doc in results)
    
    result = await extract_agent.run(all_content)
    return result.output