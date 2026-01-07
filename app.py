import streamlit as st
from main import *
import time

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("Chat With Your Document")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    # with open("temp.pdf", "wb") as f:
    #     f.write(uploaded_file.read())

    documents = load_document(uploaded_file)
    chunks = chunk_doc(documents)
    embeddings = create_embeddings()
    vector_db = store_embeddings(chunks, embeddings)
    retriever = retriever(vector_db)
    qa_chain = rag_chain(retriever)

    question = st.text_area("Ask a question", height=120)

    if st.button("Ask"):
        with st.spinner(f"Generating answer..."):
            answer = ask_qna(qa_chain, question)
            st.success("Answer generated")
            st.session_state.chat_history.append({"Question": question, "Answer": answer})

    for chat in reversed(st.session_state.chat_history):
        st.markdown("**You:**")
        st.write(chat["Question"])

        st.markdown("**Assistant:**")
        st.write(chat["Answer"])

        st.markdown("---")

    if st.button("Clear chat"):
        st.session_state.chat_history = []
