# Policy Ingestion and Retrieval Engine

This project implements a Retrieval-Augmented Generation (RAG) system for querying policy documents.

## 📁 Directory Structure
```
policy-ingestion-pipeline/
├── src/              # Source code (ingestion & retrieval)
├── app/              # CLI Application
├── data/             # Data storage (raw PDFs)
├── vectorstore/      # Persisted FAISS index
├── libs/             # Local libraries (custom fix for environment)
└── TROUBLESHOOTING.md
```

## 🚀 Quick Start (Fresh Run)

If you have closed everything, follow these exact steps:

### Step 1: Start Database (Ollama)
Open a **new, separate terminal window** and run:
```powershell
& "C:\Users\Asus\AppData\Local\Programs\Ollama\ollama.exe" serve
```
*(Keep this window open. It acts as the database server.)*

### Step 2: Run Chat App
Open your **main terminal** (inside this folder) and run:
```powershell
python app/cli.py
```

---

## ⚙️ Setup (First Time Only)
If you haven't processed the PDF yet (or want to reset):
```powershell
python src/ingestion/run_ingestion.py
```

## 🛠 Features
-   **Ingestion (Week 1)**: Robust PDF loaders & standard chunks.
-   **Retrieval (Week 2)**: Strict guardrails against hallucination.
-   **Local Dependencies**: Uses `libs/` to avoid Python version conflicts.

## ❓ Troubleshooting
-   **Ollama Error**: If connection fails, ensure Step 1 is running.
-   **Imports Error**: If you see "ModuleNotFoundError", ensure you are running python from the project root so it finds `libs/`.
