from src.retrieval.vectorstore_loader import load_vectorstore
from src.config.settings import TOP_K

def get_retriever():
    """
    Returns a configured LangChain retriever.
    """
    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": TOP_K}
    )
    return retriever
