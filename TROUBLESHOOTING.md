# Troubleshooting Guide

## "ModuleNotFoundError: No module named 'langchain.chains'"

If you see this error, it means your Python environment is picking up a corrupted or incompatible version of `langchain`.

### Solution 1: Use a Virtual Environment (Recommended)

1.  **Delete existing venv** (if safe):
    ```powershell
    Remove-Item -Recurse -Force venv
    ```
2.  **Create a new venv**:
    ```powershell
    python -m venv venv
    ```
3.  **Activate it**:
    ```powershell
    .\venv\Scripts\Activate.ps1
    ```
4.  **Install dependencies**:
    ```powershell
    pip install -r requirements.txt
    ```
5.  **Run the app**:
    ```powershell
    python app/cli.py
    ```

### Solution 2: Force Reinstall User Packages

If you are not using a venv, your user packages might be conflicted.

```powershell
pip uninstall -y langchain langchain-community langchain-core
pip install langchain langchain-community langchain-core faiss-cpu pypdf
```

## "ConnectionRefusedError" (Ollama)

If you see connection errors:

1.  Ensure Ollama is running:
    ```powershell
    ollama serve
    ```
2.  Ensure models are pulled:
    ```powershell
    ollama pull nomic-embed-text
    ollama pull mistral
    ```
