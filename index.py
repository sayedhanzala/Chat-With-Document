import os
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate


def load_document(file_path: str):
    suffix = os.path.splitext(file_path)[-1].lower()

    if suffix == ".pdf":
        loader = PyPDFLoader(file_path)
    elif suffix == ".docx":
        loader = Docx2txtLoader(file_path)
    else:
        raise ValueError("Unsupported file type")

    doc = loader.load()
    return doc


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
    store = FAISS.from_documents(chunks, embeddings)
    return store


def build_rag_chain(vector_db):
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})
    llm = ChatOllama(model="phi3", temperature=0)

    prompt = ChatPromptTemplate.from_template(
        """
    Answer the question using only the context below.
    If the answer is not present, say "I don't know".

    Context:
    {context}

    Question:
    {input}
    """
    )

    document_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(retriever, document_chain)


def ask_qna(rag_chain, question: str):
    response = rag_chain.invoke({"input": question})
    return response["answer"]
