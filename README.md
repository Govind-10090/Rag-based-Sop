# RAG-Based SOP Assistant

## Overview
This project implements a Retrieval-Augmented Generation (RAG) system for Standard Operating Procedures (SOPs).
It ingests PDF policies, provides a chat interface, and exposes a streaming API.

## Features
- **Auto-Ingestion**: Automatically processes PDFs in `data/raw`.
- **RAG Pipeline**: Uses LangChain, FAISS, and Ollama.
- **FastAPI Backend**: Exposes `/chat` endpoint with streaming.
- **Citations**: Returns source document and page number with every answer.
- **Rate Limiting**: Protects API with 10 requests/minute limit.
- **Dockerized**: Ready for container deployment.

## Installation

1. **Prerequisites**
   - Python 3.9+
   - Ollama (running locally)

2. **Setup**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ingestion**
   Run the ingestion pipeline to create the vector index:
   ```bash
   python src/ingestion/run_ingestion.py
   ```

## Running the API

Start the FastAPI server:
```bash
python -m uvicorn app.main:app --reload
```
The API is available at `http://localhost:8000`.

### API Endpoints

#### POST `/chat`
Streams the response in NDJSON format (newline delimited JSON).

**Request:**
```json
{
  "query": "What is the leave policy?",
  "chat_history": []
}
```

**Response Stream:**
```json
{"type": "citations", "content": [{"source": "policies.pdf", "page": 1, "content": "..."}]}
{"type": "token", "content": "The"}
{"type": "token", "content": " leave"}
...
```

## Docker

Build and run the container:
```bash
docker build -t rag-sop-app .
docker run -p 8000:8000 rag-sop-app
```

## Rate Limiting
The API is rate-limited to **10 requests per minute** by default.
Exceeding this limit returns a `429 Too Many Requests` status.
