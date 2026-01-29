# Resume chat

Let a user upload a resume, cover letter and similar documents and then construct a custom summarization page of this profil

---



# Resume Chat

A conversational interface for interacting with resume and cover letter data using natural language queries. Built with FastAPI, Streamlit, and LanceDB vector database with Gemini embeddings.

## Overview

Resume Chat allows users to:

- Upload resume and cover letter documents (PDF or TXT)
- Ask natural language questions about the candidate's experience, skills, and background
- Get contextual responses based on the document content
- Manage multiple documents through an intuitive web interface

The system uses semantic search with vector embeddings to retrieve relevant information and generate accurate responses.

## Project Structure

Resume_chat/
├── backend/
│   ├── app/
│   │   ├──  **init** .py
│   │   ├── chat.py              # Chat agent and retrieval logic
│   │   ├── models.py            # Pydantic data models
│   │   └── constants.py         # Configuration constants
│   └── data/                    # Resume storage directory
├── frontend/
│   └── front_chat.py            # Streamlit UI
├── knowledge_base/              # Vector database storage (gitignored)
├── api.py                       # FastAPI backend entry point
├── ingestion.py                 # Script to ingest documents into vector DB
├── pdf_to_text.py               # PDF extraction utility
├── .env                         # Environment variables (gitignored)
├── .gitignore
├── pyproject.toml               # Project dependencies
├── uv.lock                      # Locked dependencies
└── README.md

## Prerequisites

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Google Gemini API key

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd Resume_chat
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```bash
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 4. Initialize the vector database

Place your resume/cover letter files (PDF or TXT) in `backend/data/`, then run:

```bash
# Convert PDFs to text
uv run python pdf_to_text.py

# Ingest documents into vector database
uv run python ingestion.py
```

## Running the Application

The application consists of two services that need to run simultaneously:

### Terminal 1: Start the Backend API

```bash
uv run uvicorn api:app --reload
```

The API will be available at `http://127.0.0.1:8000`

### Terminal 2: Start the Frontend

```bash
uv run streamlit run frontend/front_chat.py
```

The web interface will be available at `http://localhost:8501`

## Usage

### Uploading Documents

1. Open the Streamlit interface at `http://localhost:8501`
2. Use the sidebar to upload PDF or TXT files
3. Click "Process Uploads" to ingest the documents

### Asking Questions

Type questions in the chat interface such as:

* "What experience do you have with Python?"
* "Tell me about your education background"
* "What projects have you worked on?"

The system will search the vector database and provide contextual answers based on the resume content.

## API Endpoints

### POST /chat/query

Query the resume data with natural language questions.

**Request:**

```json
{
  "prompt": "What programming languages do you know?"
}
```

**Response:**

```json
{
  "answer": "Based on my resume, I have experience with..."
}
```

### POST /upload

Upload and process resume/cover letter files.

**Request:** Multipart form data with file attachment

**Response:**

```json
{
  "status": "success",
  "filename": "resume.pdf"
}
```

## Technology Stack

* **Backend:** FastAPI, Pydantic-AI
* **Frontend:** Streamlit
* **Vector Database:** LanceDB
* **Embeddings:** Google Gemini (gemini-embedding-001)
* **LLM:** Google Gemini 2.5 Flash
* **PDF Processing:** pypdf
* **Package Manager:** uv

## Development

### Project Dependencies

Core dependencies are managed in `pyproject.toml`:

* FastAPI for REST API
* Streamlit for web UI
* LanceDB for vector storage
* Pydantic-AI for agent framework
* pypdf for PDF text extraction

### Adding New Documents

You can add documents in two ways:

1. **Via Web Interface:** Use the upload feature in the Streamlit sidebar
2. **Via Scripts:** Place files in `backend/data/` and run the ingestion scripts

### Vector Database

The vector database stores embeddings of resume content in the `knowledge_base/` directory. This directory is gitignored as it contains generated data and can be recreated by running the ingestion script.

## Configuration

Key configuration values in `backend/app/constants.py`:

* `DATA_PATH`: Location of source documents
* `VECTOR_DATABASE_PATH`: Location of vector database

Embedding configuration in `backend/app/models.py`:

* Model: gemini-embedding-001
* Dimension: 3072

## Troubleshooting

### Connection Errors

Ensure both the backend API and frontend are running. The frontend expects the backend at `http://127.0.0.1:8000`.

### Empty Responses

Make sure documents have been ingested into the vector database. Run `ingestion.py` to process files in `backend/data/`.

### API Rate Limits

The ingestion script includes a 25-second delay between documents to avoid API rate limits. Adjust this in `ingestion.py` if needed.
