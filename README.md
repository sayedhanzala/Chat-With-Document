# Document Question Answering System using RAG (Local LLM)

## Overview

This project implements a Retrieval-Augmented Generation (RAG) system that allows users to upload a document and ask questions based strictly on the document’s content.

The system is fully local, uses no external APIs, has no rate limits, and performs inference using an open-source Large Language Model.

---

## Key Features

- Upload PDF/Word documents
- Semantic chunking and retrieval
- Answers grounded strictly in document context
- Local LLM inference using Ollama
- No API keys required
- Session-based chat history
- Simple Streamlit user interface

---

## Tech Stack

- Python 3.9+
- Streamlit
- LangChain (modern LCEL-based chains)
- FAISS (vector database)
- Hugging Face sentence-transformers (embeddings)
- Ollama (local LLM runtime)
- Phi-3 (local LLM)

---

## Project Structure
```
Chat-With-Document/
│
├── app.py
├── main.py
├── requirements.txt
└── README.md
```
---

## Prerequisites

- Python 3.9 or higher
- Minimum 8 GB RAM recommended
- Internet connection for initial model download

---

## Setup Instructions

### 1. Code Setup

```bash
git clone https://github.com/sayedhanzala/Chat-With-Document.git
cd Chat-With-Document

## Windows:
python -m venv venv
venv\Scripts\activate

## Linux / macOS:
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

---

### 2. Ollama Setup

```bash
## Download and install Ollama from:
https://ollama.com

### Restart the terminal after installation.

## Verify installation:
ollama --version
```


---

### 3. Download Required Model

```bash
## This project uses the Phi-3 model.

ollama pull phi3

## Verify:
ollama list
```

---

### 4. Optional Manual Test

```bash
ollama run phi3
```
Type a simple prompt to confirm it works, then exit with /bye.

---

## Running the Application
```bash
streamlit run app.py
```

---

The application will open in your default browser.

---

## How to Use

1. Upload a PDF/Word document
2. Enter a question in the text area
3. Submit the question
4. View the generated answer
5. Ask follow-up questions (chat history preserved)

All answers are generated strictly from the uploaded document.

---

## Model and Retrieval Details

- LLM: Phi-3 via Ollama
- Embeddings: sentence-transformers/all-MiniLM-L6-v2
- Vector Store: FAISS (in-memory)
- Inference: Local CPU-based

---

## Notes

- No external APIs are used
- First response may be slower due to model warm-up
- Subsequent responses are faster
- Chat history is session-based

---

## License

This project is intended for educational and personal use.
