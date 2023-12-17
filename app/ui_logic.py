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

from app.ml_logic.model import run_model


def display_messages():
    st.subheader("Magic happens here!")
    for i, (msg, is_user) in enumerate(st.session_state["messages"]):
        message(msg, is_user=is_user, key=str(i))
    st.session_state["thinking_spinner"] = st.empty()


def process_input():

    if st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
        print(f'User input: {st.session_state["user_input"]}')
        query = st.session_state["user_input"].strip()
        print(f'Query: {query}')

        with st.session_state["thinking_spinner"], st.spinner(f"Thinking"):
            output = run_model(query)
        st.session_state["messages"].append((query, True))
        st.session_state["messages"].append((output, False))
        print(f'********** Session messages: {st.session_state["messages"]}')
        st.session_state["user_input"] = None


def is_openai_api_key_set() -> bool:
    return len(st.session_state["OPENAI_API_KEY"]) > 0
