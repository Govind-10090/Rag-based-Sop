from pydantic import BaseModel, Field
from typing import List, Optional

class SearchResult(BaseModel):
    source: str = Field(..., description="The source document filename")
    page: Optional[int] = Field(None, description="The page number in the source document")
    content: str = Field(..., description="The snippet content used")

class ChatRequest(BaseModel):
    query: str = Field(..., description="The user's question", min_length=1)
    chat_history: List[List[str]] = Field([], description="List of [user, bot] turn pairs")

class ChatResponse(BaseModel):
    response: str = Field(..., description="The RAG generated response")
    citations: Optional[List[SearchResult]] = Field(None, description="List of sources used")
