from os import path
import streamlit as st
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings

from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.params import *


def create_retriever():
    print(f'Loading documents from {PDF_PATH}')
    loader = PyPDFDirectoryLoader(PDF_PATH)
    documents = loader.load()
    print(f'Loaded {len(documents)} documents')

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=100)
    all_splits = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(
        openai_api_key=st.session_state["OPENAI_API_KEY"])
    retriever = Chroma.from_documents(
        all_splits, embeddings).as_retriever()
    print(f'Created retriever: {retriever}')
    return retriever
