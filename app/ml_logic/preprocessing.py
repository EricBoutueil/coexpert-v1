import streamlit as st

from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

from params import *


def load_pdf():
    '''Load pdf files from source folder'''
    print(f'Loading pages from {PDF_PATH}')
    loader = PyPDFDirectoryLoader(PDF_PATH)
    pages = loader.load()
    print(f'Loaded {len(pages)} pages')
    return pages


def split_pdf(pages):
    '''Preprocess pdf files'''
    # split the pages in small chunks
    # Change the chunk_size and chunk_overlap as needed
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=100)
    all_splits = text_splitter.split_documents(pages)
    print(f"Created {len(all_splits)} splits")
    # TODO: cache/local stoarage of the splits?
    return all_splits


def create_embeddings():
    '''Create the embeddings'''
    print(f'****openai_api_key: {st.session_state["OPENAI_API_KEY"]}')
    embeddings = OpenAIEmbeddings(
        openai_api_key=st.session_state["OPENAI_API_KEY"])
    print(f'Created embeddings')
    # TODO: Using embedded DuckDB without persistence: data will be transient -> cache/local storage ?
    return embeddings


def create_retriever(all_splits, embeddings):
    '''Create the retriever'''
    retriever = Chroma.from_documents(
        all_splits, embeddings).as_retriever()
    print(f'Created retriever: {retriever}')
    return retriever


def preprocess_pdf_to_retriever():
    '''Preprocess pdf files to retriever'''''
    pages = load_pdf()
    all_splits = split_pdf(pages)
    embeddings = create_embeddings()
    retriever = create_retriever(all_splits, embeddings)
    return retriever
