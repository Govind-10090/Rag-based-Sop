from langchain_community.vectorstores import FAISS
import os
from src.config.settings import FAISS_INDEX_PATH

def create_and_save_index(chunks, embeddings):
    """
    Creates a FAISS index from chunks and saves it to disk.
    """
    if not chunks:
        print("Warning: No chunks to index.")
        return

    vectorstore = FAISS.from_documents(chunks, embeddings)
    
    # Ensure directory exists (FAISS saves to a folder)
    os.makedirs(os.path.dirname(FAISS_INDEX_PATH), exist_ok=True)
    
    vectorstore.save_local(str(FAISS_INDEX_PATH))
    print(f"✅ Index saved to {FAISS_INDEX_PATH}")
