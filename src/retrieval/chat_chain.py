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
        self.llm = ChatOllama(model=LLM_MODEL_NAME, temperature=0, keep_alive="5m")
        self.retriever = get_retriever()
        
        # 1. History Contextualization
        contextualize_q_system_prompt = """Given a chat history and the latest user question \
which might reference context in the chat history, formulate a standalone question \
which can be understood without the chat history. Do NOT answer the question, \
just reformulate it if needed and otherwise return it as is."""
        
        self.contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                ("placeholder", "{chat_history}"),
                ("human", "{input}"),
            ]
        )
        
        self.history_chain = self.contextualize_q_prompt | self.llm | StrOutputParser()
        
        # 2. Answer Generation
        self.qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_TEMPLATE),
                ("human", "{input}"),
            ]
        )

    async def astream(self, question, chat_history=[]):
        formatted_history = []
        for q, a in chat_history:
            formatted_history.append(HumanMessage(content=q))
            formatted_history.append(AIMessage(content=a))
            
        # 1. Determine Query
        if chat_history:
            query = await self.history_chain.ainvoke({"input": question, "chat_history": formatted_history})
        else:
            query = question
            
        # 2. Retrieve
        docs = await self.retriever.ainvoke(query)
        
        # 3. Yield Citations
        citations = []
        for doc in docs:
            citations.append({
                "source": doc.metadata.get("source", "Unknown"),
                "page": doc.metadata.get("page", None),
                "content": doc.page_content[:200]
            })
        
        yield {"type": "citations", "content": citations}
        
        # 4. Generate Answer
        context_str = format_docs(docs)
        
        # Create the prompt value
        prompt_value = await self.qa_prompt.ainvoke({"context": context_str, "input": question})
        
        async for chunk in self.llm.astream(prompt_value):
            yield {"type": "token", "content": chunk.content}

    def ask(self, question, chat_history=[]):
        # Fallback synchronous/blocking implementation if needed (not recommended for API)
        import asyncio
        return asyncio.run(self.astream(question, chat_history))

