import streamlit as st

from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

from app.params import *

import pickle

import time


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

    os.makedirs('./preprocess_cache/', exist_ok=True)
    cache_path = "./preprocess_cache/all_splits_cache.pkl"
    with open(cache_path, "wb") as f:
        pickle.dump(all_splits, f)
        print(f'Saved all splits to cache folder: {cache_path}')

    return all_splits


def load_all_splits_cache():
    '''Load the all splits from cache'''
    cache_path = "./preprocess_cache/all_splits_cache.pkl"
    try:
        with open(cache_path, "rb") as f:
            all_splits = pickle.load(f)
            print(f'Loaded from cache: {len(all_splits)} splits')
            return all_splits
    except FileNotFoundError:
        pages = load_pdf()
        all_splits = split_pdf(pages)
        return all_splits


def create_embeddings():
    '''Create the embeddings'''
    embeddings = OpenAIEmbeddings(
        openai_api_key=st.session_state["OPENAI_API_KEY"])
    print(f'Created embeddings')
    # TODO: Using embedded DuckDB without persistence: data will be transient -> cache/local storage ?
    return embeddings


def create_retriever(all_splits, embeddings):
    '''Create the retriever'''
    retriever = Chroma.from_documents(
        all_splits, embeddings, persist_directory="./preprocess_cache/chroma_db").as_retriever()
    print(f'Created retriever: {retriever}')
    return retriever


def preprocess_pdf_to_retriever(start_time):
    '''Preprocess pdf files to retriever'''
    print("---------- %s seconds ----------" % (time.time() - start_time))
    if not os.path.exists('./preprocess_cache/all_splits_cache.pkl'):
        print("No pdf splits found. Loading pdf and creating splits...")
        pages = load_pdf()
        print("---------- %s seconds ----------" % (time.time() - start_time))
        all_splits = split_pdf(pages)
        print("---------- %s seconds ----------" % (time.time() - start_time))
    else:
        print("Pdf splits found. Loading splits...")
        all_splits = load_all_splits_cache()
        print("---------- %s seconds ----------" % (time.time() - start_time))

    embeddings = create_embeddings()
    print("---------- %s seconds ----------" % (time.time() - start_time))
    retriever = create_retriever(all_splits, embeddings)
    print("---------- %s seconds ----------" % (time.time() - start_time))
    return retriever
