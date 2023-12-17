import os
import tempfile
import streamlit as st
from streamlit_chat import message
# from pdfquery import PDFQuery
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import UnstructuredPDFLoader
# from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain

from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]


def display_messages():
    st.subheader("Magic happens here!")
    for i, (msg, is_user) in enumerate(st.session_state["messages"]):
        message(msg, is_user=is_user, key=str(i))
    st.session_state["thinking_spinner"] = st.empty()


def process_input():

    if st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
        print(f'User input: {st.session_state["user_input"]}')
        # user_text = st.session_state["user_input"].strip()
        query = st.session_state["user_input"].strip()
        print(f'Query: {query}')
        retriever = st.session_state["retriever"]
        print(f'Using retriever: {retriever}')

        with st.session_state["thinking_spinner"], st.spinner(f"Thinking"):
            # query_text = st.session_state["pdfquery"].ask(user_text)
            docs = retriever.get_relevant_documents(query)
            print(f'Found {len(docs)} relevant documents')
            chain = load_qa_chain(ChatOpenAI(
                temperature=0, openai_api_key=OPENAI_API_KEY), chain_type="stuff")
            output = chain.run(input_documents=docs, question=query)
        st.session_state["messages"].append((query, True))
        st.session_state["messages"].append((output, False))


def read_and_save_file():
    st.session_state["pdfquery"].forget()  # to reset the knowledge base
    st.session_state["messages"] = []
    st.session_state["user_input"] = ""

    for file in st.session_state["file_uploader"]:
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tf.write(file.getbuffer())
            file_path = tf.name

        with st.session_state["ingestion_spinner"], st.spinner(f"Ingesting {file.name}"):
            st.session_state["pdfquery"].ingest(file_path)
        os.remove(file_path)


def is_openai_api_key_set() -> bool:
    return len(st.session_state["OPENAI_API_KEY"]) > 0
