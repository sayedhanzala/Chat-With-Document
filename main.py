from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama
from langchain_classic.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
import tempfile
import os


def load_document(file):
    suffix = os.path.splitext(file.name)[-1].lower()

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(file.read())
        tmp_path = tmp.name

    if suffix == ".pdf":
        loader = PyPDFLoader(tmp_path)
    elif suffix == ".docx":
        loader = Docx2txtLoader(tmp_path)
    else:
        raise ValueError("Unsupported file type")

    documents = loader.load()
    return documents


def chunk_doc(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(docs)
    return chunks


def create_embeddings():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return embeddings


def store_embeddings(chunks, embeddings):
    vector_db = FAISS.from_documents(chunks, embeddings)
    return vector_db


def retriever(vector):
    retriever = vector.as_retriever(search_kwargs={"k": 3})
    return retriever


def rag_chain(retriever):
    llm = ChatOllama(temperature=0, model="phi3")

    prompt = ChatPromptTemplate.from_template("""
    Answer the question using only the context below.
    If the answer is not present, say "I don't know".

    Context:
    {context}

    Question:
    {input}
    """)

    document_chain = create_stuff_documents_chain(llm, prompt)
    qa_chain = create_retrieval_chain(retriever, document_chain)

    return qa_chain

def ask_qna(qa_chain, question):
    response = qa_chain.invoke({"input": question})
    return response["answer"]
