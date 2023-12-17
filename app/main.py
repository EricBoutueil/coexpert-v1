import os
import streamlit as st
from ui_logic import display_messages, process_input, is_openai_api_key_set
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

from app.params import *
from ml_logic.retriever import create_retriever

st.set_page_config(page_title="CoExpert")


def main():
    if len(st.session_state) == 0:
        main_path = os.path.dirname(__file__)
        print("Creating retriever")
        # TODO: change nber_pdf into a global variable
        retriever = create_retriever(main_path, nber_pdf=11)
        print("Initializing session state")
        st.session_state["OPENAI_API_KEY"] = OPENAI_API_KEY
        st.session_state["retriever"] = retriever
        st.session_state["messages"] = []

        # if is_openai_api_key_set():
        #     st.session_state["pdfquery"] = PDFQuery(
        #         st.session_state["OPENAI_API_KEY"])
        # else:
        #     st.session_state["pdfquery"] = None
    else:
        print("Session state already initialized")

    st.header("Welcome to CoExpert")

    display_messages()
    st.text_input("Please enter your question:", key="user_input",
                  disabled=not is_openai_api_key_set(), on_change=process_input)

    st.divider()


if __name__ == "__main__":
    main()
