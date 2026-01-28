import sys
print(sys.path)
try:
    import langchain
    print(f"Langchain: {langchain}")
    print(f"Langchain file: {langchain.__file__}")
    print(f"Langchain dir: {dir(langchain)}")
    import langchain.chains
    print("langchain.chains imported!")
except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Error: {e}")
