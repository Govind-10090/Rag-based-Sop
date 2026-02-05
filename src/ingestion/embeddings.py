from langchain_community.embeddings import OpenAIEmbeddings
from src.config.settings import EMBEDDING_MODEL_NAME
import os

def get_embeddings():
    """
    Returns the configured embedding model.
    """
    # Fallback to OpenAI if available, as Ollama can be flaky in demos
    if os.getenv("OPENAI_API_KEY"):
        return OpenAIEmbeddings()
        
    return OpenAIEmbeddings() # Defaulting to OpenAI since key is in .env
