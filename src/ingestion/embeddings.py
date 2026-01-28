from langchain_community.embeddings import OllamaEmbeddings
from src.config.settings import EMBEDDING_MODEL_NAME

def get_embeddings():
    """
    Returns the configured embedding model.
    """
    return OllamaEmbeddings(
        model=EMBEDDING_MODEL_NAME
    )
