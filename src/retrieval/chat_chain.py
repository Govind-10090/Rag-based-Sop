import sys
from langchain_community.chat_models import ChatOllama
from src.retrieval.retriever import get_retriever
from src.retrieval.prompt import get_chat_prompt, SYSTEM_TEMPLATE
from src.config.settings import LLM_MODEL_NAME
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableBranch
from langchain_core.messages import HumanMessage, AIMessage

# --- Custom Implementation of Chains (to bypass broken langchain install) ---

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

class ChatChain:
    def __init__(self):
        self.llm = ChatOllama(model=LLM_MODEL_NAME, temperature=0)
        self.retriever = get_retriever()
        self.chain = self._build_chain()

    def _build_chain(self):
        # 1. History Contextualization
        contextualize_q_system_prompt = """Given a chat history and the latest user question \
which might reference context in the chat history, formulate a standalone question \
which can be understood without the chat history. Do NOT answer the question, \
just reformulate it if needed and otherwise return it as is."""
        
        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                ("placeholder", "{chat_history}"),
                ("human", "{input}"),
            ]
        )
        
        history_chain = contextualize_q_prompt | self.llm | StrOutputParser()
        
        # 2. Retriever Logic
        # If chat_history is empty, use input directly. If present, use history_chain.
        def get_query(input_dict):
            if input_dict.get("chat_history"):
                return history_chain
            else:
                return input_dict["input"]

        # This runnable takes input_dict, generates query, and passes to retriever
        retriever_chain = RunnableBranch(
            (lambda x: bool(x.get("chat_history")), history_chain | self.retriever),
            (lambda x: not bool(x.get("chat_history")), (lambda x: x["input"]) | self.retriever),
            (lambda x: x["input"]) | self.retriever # Fallback
        )

        # 3. Answer Generation
        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_TEMPLATE),
                ("human", "{input}"),
            ]
        )
        
        # We need to map:
        # "context": retriever_chain
        # "input": input
        # "chat_history": (passed through but not used in final answer prompt directly, or is it?)
        # The prompt only uses {context} and {question} (mapped to {input} here).
        
        rag_chain = (
            RunnablePassthrough.assign(
                context=retriever_chain | format_docs
            )
            | qa_prompt
            | self.llm
            | StrOutputParser()
        )
        
        return rag_chain

    def ask(self, question, chat_history=[]):
        formatted_history = []
        for q, a in chat_history:
            formatted_history.append(HumanMessage(content=q))
            formatted_history.append(AIMessage(content=a))
            
        return self.chain.invoke({"input": question, "chat_history": formatted_history})
