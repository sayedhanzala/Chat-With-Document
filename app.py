import streamlit as st
import tempfile
import os

from index import (
    load_document,
    chunk_doc,
    create_embeddings,
    store_embeddings,
    build_rag_chain,
    ask_qna,
)

st.set_page_config(page_title="Chat With Your Document")

if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("Chat With Your Document")

uploaded_file = st.file_uploader("Upload a PDF or DOCX", type=["pdf", "docx"])

if uploaded_file and st.session_state.rag_chain is None:
    suffix = os.path.splitext(uploaded_file.name)[-1].lower()

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    with st.spinner("Indexing document..."):
        documents = load_document(tmp_path)
        chunks = chunk_doc(documents)
        embeddings = create_embeddings()
        vector_db = store_embeddings(chunks, embeddings)
        st.session_state.rag_chain = build_rag_chain(vector_db)

    os.remove(tmp_path)
    st.success("Document indexed successfully")

if st.session_state.rag_chain:
    question = st.text_area("Ask a question", height=120)

    if st.button("Ask"):
        with st.spinner("Generating answer..."):
            answer = ask_qna(st.session_state.rag_chain, question)

        st.session_state.chat_history.append({"question": question, "answer": answer})

    for chat in reversed(st.session_state.chat_history):
        st.markdown("**You:**")
        st.write(chat["question"])
        st.markdown("**Assistant:**")
        st.write(chat["answer"])
        st.markdown("---")

    if st.button("Clear chat"):
        st.session_state.chat_history = []
