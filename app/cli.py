import sys
import os

# Add local libs to path to ensure correct versions are used
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'libs'))
# Add project root to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.retrieval.chat_chain import ChatChain
import time

def main():
    print("Initializing Chatbot... (this may take a moment)")
    try:
        chat_bot = ChatChain()
    except Exception as e:
        print(f"❌ Error initializing chat chain: {e}")
        print("Ensure Ollama is running and models (mistral, nomic-embed-text) are pulled.")
        return

    print("\n🤖 Policy Assistant Ready! Type 'exit' to quit.\n")
    
    chat_history = []
    
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit", "q"]:
                print("Goodbye!")
                break
            
            if not user_input.strip():
                continue

            print("Assistant: ", end="", flush=True)
            
            # Start timing/processing indicator if needed
            # response = chat_bot.ask(user_input, chat_history) 
            
            # The chain handles history management internally typically via Memory, 
            # but standard ConvRetrievalChain usually takes a list of tuples (q, a) as 'chat_history' arg
            # IF using external memory management. 
            # Our ChatChain uses ConversationBufferMemory internally, so we might pass empty list 
            # OR we configured it to use internal memory.
            # Let's check ChatChain implementation...
            # It creates 'rag_chain' which is a Runnable.
            # We call invoke with verify "chat_history" in input?
            # create_history_aware_retriever expects 'chat_history'.
            # If we don't pass it, it might fail if the prompt expects it.
            # But we aren't using a RunnableWithMessageHistory wrapper.
            # So we must manage history manually or pass it.
            
            # Implementation in ChatChain.ask:
            # response = self.chain.invoke({"input": question, "chat_history": chat_history})
            # So we need to pass chat_history.
            
            response = chat_bot.ask(user_input, chat_history)
            
            print(response)
            print("-" * 50)
            
            # Update history
            chat_history.append((user_input, response))
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
