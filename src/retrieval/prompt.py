from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate

SYSTEM_TEMPLATE = """You are a Retrieval-Augmented AI assistant.
Answer only using the retrieved context.

If the answer is not in the context, respond exactly:
"I don’t have enough information in the provided documents to answer that."

Do not guess, infer, or use external knowledge.

Context:
{context}
"""

def get_chat_prompt():
    """
    Returns the strict system prompt for the chat chain.
    """
    messages = [
        ("system", SYSTEM_TEMPLATE),
        ("human", "{question}"),
    ]
    return ChatPromptTemplate.from_messages(messages)
