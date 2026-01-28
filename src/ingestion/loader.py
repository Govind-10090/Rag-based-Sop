from langchain_community.document_loaders import PyPDFLoader
import os

def load_documents(file_path):
    """
    Loads a PDF file and returns a list of documents.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    loader = PyPDFLoader(file_path)
    return loader.load()
