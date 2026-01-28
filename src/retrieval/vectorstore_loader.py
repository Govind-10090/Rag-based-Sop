from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from src.config.settings import FAISS_INDEX_PATH, EMBEDDING_MODEL_NAME
import os
import sys

def load_vectorstore():
    """
    Loads the persisted FAISS vector store.
    Fails loudly if the index is missing.
    """
    if not os.path.exists(FAISS_INDEX_PATH):
        print(f"❌ Error: FAISS index not found at {FAISS_INDEX_PATH}")
        print("Run 'python src/ingestion/run_ingestion.py' first.")
        sys.exit(1)
        
    try:
        embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL_NAME)
        vectorstore = FAISS.load_local(
            str(FAISS_INDEX_PATH), 
            embeddings,
            allow_dangerous_deserialization=True
        )
        return vectorstore
    except Exception as e:
        print(f"❌ Error loading vector store: {e}")
        sys.exit(1)
