from os import path
import streamlit as st
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings

from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def create_retriever(main_path, nber_pdf=2):
    raw_data_folder = path.join(main_path, 'raw_data')
    pdf_folder = f'{nber_pdf}_pdf'
    path_to_pdf = path.join(raw_data_folder, pdf_folder)
    print(f'Loading documents from {path_to_pdf}')
    loader = PyPDFDirectoryLoader(path_to_pdf)
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
