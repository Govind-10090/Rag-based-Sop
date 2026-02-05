import os
import logging
import json
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from app.models import ChatRequest
from src.retrieval.chat_chain import ChatChain
from dotenv import load_dotenv

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RAG_API")

# Load env variables
load_dotenv()

# Rate Limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="RAG SOP Assistant", version="1.0.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ChatChain lazily or on startup?
# On startup better to avoid re-init per request if heavyweight
chat_chain = None

@app.on_event("startup")
async def startup_event():
    global chat_chain
    logger.info("Initializing ChatChain...")
    try:
        chat_chain = ChatChain()
        logger.info("ChatChain initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize ChatChain: {e}")
        raise e

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/chat")
@limiter.limit("10/minute")
async def chat_endpoint(request: Request, body: ChatRequest):
    if not chat_chain:
        raise HTTPException(status_code=500, detail="Chat system not initialized")
    
    logger.info(f"Received query: {body.query}")
    
    async def generate():
        try:
            async for chunk in chat_chain.astream(body.query, body.chat_history):
                # chunk is now a dict {"type": "...", "content": "..."}
                yield json.dumps(chunk) + "\n"
        except Exception as e:
            logger.error(f"Error during streaming: {e}")
            yield json.dumps({"type": "error", "content": str(e)}) + "\n"

    return StreamingResponse(generate(), media_type="application/x-ndjson")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
