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

st.set_page_config(page_title="CoExpert")


def main():
    if len(st.session_state) == 0:
        st.session_state["OPENAI_API_KEY"] = OPENAI_API_KEY
        st.session_state["messages"] = []

        # path = './raw_data'
        path = '/Users/ericboutueil/code/EricBoutueil/coexpert-v1/app/raw_data/2_pdf'
        loader = PyPDFDirectoryLoader(path)
        documents = loader.load()
        print(f'Loaded {len(documents)} documents')

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=100)
        all_splits = text_splitter.split_documents(documents)

        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        retriever = Chroma.from_documents(
            all_splits, embeddings).as_retriever()
        print(f'Created retriever: {retriever}')

        st.session_state["retriever"] = retriever

        # if is_openai_api_key_set():
        #     st.session_state["pdfquery"] = PDFQuery(
        #         st.session_state["OPENAI_API_KEY"])
        # else:
        #     st.session_state["pdfquery"] = None
    else:
        print("Session state already initialized")

    st.header("Welcome to CoExpert")

    # st.subheader("Upload a document")
    # st.file_uploader(
    #     "Upload document",
    #     type=["pdf"],
    #     key="file_uploader",
    #     on_change=read_and_save_file,
    #     label_visibility="collapsed",
    #     accept_multiple_files=True,
    #     disabled=not is_openai_api_key_set(),
    # )

    # st.session_state["ingestion_spinner"] = st.empty()

    display_messages()
    st.text_input("Please enter your question:", key="user_input",
                  disabled=not is_openai_api_key_set(), on_change=process_input)

    st.divider()


if __name__ == "__main__":
    main()
