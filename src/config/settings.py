import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Data directories
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Vector Store
VECTORSTORE_DIR = BASE_DIR / "vectorstore"
FAISS_INDEX_PATH = VECTORSTORE_DIR / "faiss_index"

# Models
EMBEDDING_MODEL_NAME = "nomic-embed-text"
LLM_MODEL_NAME = "mistral"  # Or your preferred Ollama model

# Ingestion Settings
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

# Retrieval Settings
TOP_K = 3
