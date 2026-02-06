# Resume Chat – Your Resume, Brought to Life

## Project Overview

This project is an AI-powered chatbot that lets users upload their resume and have conversations with it. The AI impersonates the person in the resume and answers questions as if it were that person.

The chatbot uses Retrieval-Augmented Generation (RAG) to answer questions based on the actual content of uploaded resumes and cover letters.

## Purpose

- Make it easier for recruiters to explore candidates through conversation
- Provide instant, contextual answers about a person's experience and skills
- Practice AI engineering with RAG architecture, vector databases and cloud deployment

## Key Features

- Chat interface for asking questions about the uploaded resume
- AI answers as if it were the person in the resume (persona mode)
- Upload support for PDF and TXT files
- Resume section browser (jobs, education, skills, projects)
- Chat history for context-aware conversations
- Rate limit handling with user-friendly error messages

## Tech Stack

| Layer           | Technology                                   |
| --------------- | -------------------------------------------- |
| Backend         | Python, FastAPI, Pydantic-AI                 |
| Frontend        | Streamlit                                    |
| AI/LLM          | Google Gemini 2.5 Flash                      |
| Embeddings      | Gemini Embedding (3072 dimensions)           |
| Vector Database | LanceDB                                      |
| Deployment      | Docker, Docker Compose, Azure Container Apps |
| Package Manager | uv                                           |
| Version Control | GitHub (branches, pull requests, issues)     |

## Data & Ethics

- Only user-uploaded documents are processed
- No personal data is stored permanently
- Content is used for retrieval, not reproduced verbatim
- AI is instructed to say "I don't know" if information is not in the resume

## Team & Workflow

- 2 developers working with GitHub flow
- Issues and pull requests for task management
- Code reviews before merging to main

## Screenshots and Description

### 1. Document Upload

Users can upload their resume (PDF or TXT) through the sidebar. The document is parsed and stored in the vector database.

![Upload](screenshots/upload.png)

### 2. Vector Database & Embeddings

When a document is uploaded, the content is embedded using Gemini's text-embedding-001 model (3072 dimensions) and stored in LanceDB.

![Models](screenshots/models.png)

### 3. The RAG Agent

The chat agent uses a system prompt to impersonate the person in the resume. It always retrieves relevant documents before answering.

![Agent](screenshots/agent.png)

### 4. The Chat Interface

The Streamlit frontend provides a modern chat experience with custom CSS, avatars, and gradient-styled message bubbles.

![Chat](screenshots/chat.png)

### 5. Resume Sections Browser

Users can browse extracted sections from the resume: jobs, internships, education, projects, and skills.

![Sections](screenshots/sections.png)

### 6. Rate Limit Handling

The application handles Gemini API rate limits gracefully, showing a friendly message instead of crashing.

![Rate Limit](screenshots/rate-limit.png)

### 7. Architecture Overview

```
┌─────────────────────────────────────────────┐
│              Streamlit Frontend             │
│   Upload │ Chat │ Sections │ Clear Chat    │
└─────────────────┬───────────────────────────┘
                  │ HTTP
┌─────────────────▼───────────────────────────┐
│              FastAPI Backend                │
│   /upload │ /chat/query │ /resume/sections │
└─────────────────┬───────────────────────────┘
                  │
    ┌─────────────┴─────────────┐
    ▼                           ▼
┌─────────┐               ┌───────────┐
│ LanceDB │               │  Gemini   │
│ Vectors │               │    API    │
└─────────┘               └───────────┘
```

---

## How to Run Locally

### 1. Clone and install

```bash
git clone https://github.com/Nverest/Resume_chat.git
cd Resume_chat/resuchat
uv sync
```

### 2. Set environment variables

Create a `.env` file:

```
GOOGLE_API_KEY=your_gemini_api_key
```

### 3. Run with Docker Compose

```bash
cd src/resuchat
docker compose up --build
```

Frontend: http://localhost:8501
Backend: http://localhost:8000

## Deployment

The application is containerized with Docker Compose (backend + frontend) and deployed to Azure Container Apps.

### Docker Compose Setup

The project uses two separate containers:

```yaml
services:
  backend:
    build:
      context: .
      dockerfile: backend/Dockerfile
    image: resuchat.azurecr.io/resuchat-backend:latest
    environment:
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}

  frontend:
    build:
      context: .
      dockerfile: frontend/Dockerfile
    image: resuchat.azurecr.io/resuchat-frontend:latest
    depends_on:
      - backend
    environment:
      - API_URL=http://backend
```

### Build and Push to Azure

```bash
# Build images
docker compose build --no-cache

# Push to Azure Container Registry
docker compose push
```

### Deployment Flow

```
Local Code → Docker Build → Azure Container Registry → Azure Container Apps
```

1. Code changes are made locally
2. Docker images are built with `docker compose build`
3. Images are pushed to Azure Container Registry
4. Azure Container Apps automatically pulls the new images

## Disclaimer

This project is created for educational purposes as part of an AI engineering course.

Free tier gemini API is being used which is limited to 5 tokens/min and 20 tokens/day

---

## Live Demo

Scan the QR code or visit:
https://resuchat-frontend-featf9bwe4gwc3f0.swedencentral-01.azurewebsites.net/

![QR Code](screenshots/QR-Code.png)
