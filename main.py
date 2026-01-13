from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel
import tempfile
import os

from index import *

app = FastAPI(title="Chat With Document")

# Global RAG state (single document for now)
rag_chain = None


class QuestionRequest(BaseModel):
    question: str


class AnswerResponse(BaseModel):
    answer: str


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    global rag_chain

    suffix = os.path.splitext(file.filename)[-1].lower()
    if suffix not in [".pdf", ".docx"]:
        raise HTTPException(
            status_code=400, detail="Only PDF and DOCX files are supported"
        )

    # Save uploaded file to temp path
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        documents = await run_in_threadpool(load_document, tmp_path)
        chunks = await run_in_threadpool(chunk_doc, documents)
        embeddings = create_embeddings()
        vector_db = await run_in_threadpool(store_embeddings, chunks, embeddings)

        # Build RAG chain ONCE
        rag_chain = build_rag_chain(vector_db)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        os.remove(tmp_path)

    return {"status": "success", "message": "Document uploaded & indexed"}


@app.post("/ask", response_model=AnswerResponse)
async def ask_question(payload: QuestionRequest):
    if rag_chain is None:
        raise HTTPException(status_code=400, detail="No document uploaded yet")

    answer = await run_in_threadpool(ask_qna, rag_chain, payload.question)

    return {"answer": answer}
