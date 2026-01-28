import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.ingestion.loader import load_documents
from src.ingestion.splitter import split_documents
from src.ingestion.embeddings import get_embeddings
from src.ingestion.indexer import create_and_save_index
from src.config.settings import RAW_DATA_DIR

def main():
    # Use existing policies.pdf if it's there, otherwise check known locations or error out
    # Based on previous file listing, data/policies.pdf might be the intent, 
    # but the new structure says data/raw. 
    # I should check if the file exists in the old location and move it, or just read from there for now and advise user to move it.
    # For this task, I'll assume we read from data/raw/policies.pdf or fall back to data/policies.pdf if not found (and maybe move it).
    
    pdf_path = os.path.join(RAW_DATA_DIR, "policies.pdf")
    
    # Check if we need to look in the old location
    old_path = os.path.join(os.path.dirname(RAW_DATA_DIR), "policies.pdf")
    if not os.path.exists(pdf_path) and os.path.exists(old_path):
        print(f"Found policies.pdf in {old_path}, using that.")
        pdf_path = old_path

    if not os.path.exists(pdf_path):
        print(f"❌ Error: policies.pdf not found in {RAW_DATA_DIR} or {old_path}")
        return

    print("🚀 Starting Ingestion Pipeline...")
    
    # 1. Load
    print("Loading documents...")
    docs = load_documents(pdf_path)
    print(f"Loaded {len(docs)} pages.")

    # 2. Split
    print("Splitting documents...")
    chunks = split_documents(docs)
    print(f"Created {len(chunks)} chunks.")

    # 3. Embed
    print("Initializing embeddings...")
    embeddings = get_embeddings()

    # 4. Index
    print("Creating and saving index...")
    create_and_save_index(chunks, embeddings)
    
    print("✅ Ingestion Complete!")

if __name__ == "__main__":
    main()
