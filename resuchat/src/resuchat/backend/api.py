from fastapi import FastAPI, UploadFile, File
from chat import chat_agent, extract_agent
from models import Prompt, Resume
from constants import DATA_PATH, VECTOR_DATABASE_PATH
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
        # Save the file
        file_path = DATA_PATH / file.filename
        content = await file.read()
        
        # If it's a PDF, extract text
        if file.filename.endswith('.pdf'):
            pdf_reader = PdfReader(io.BytesIO(content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            # Save as text file
            txt_filename = file.filename.replace('.pdf', '.txt')
            txt_path = DATA_PATH / txt_filename
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(text)
                
            # Also save original PDF
            with open(file_path, 'wb') as f:
                f.write(content)
        else:
            # Save text file directly
            with open(file_path, 'wb') as f:
                f.write(content)
            text = content.decode('utf-8')
        
        # Ingest into vector database
        db = lancedb.connect(uri=VECTOR_DATABASE_PATH)
        
        
        if "Resume" in db.table_names():
            db.drop_table("Resume")

        table = db.create_table("Resume", schema=Resume)

        doc_id = file.filename.split('.')[0].lower()

        # Add new entry
        table.add([
            {
                "doc_id": doc_id,
                "filepath": str(file_path),
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