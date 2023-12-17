# from os import path
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings

from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.params import *

# path.join(path.dirname(__file__), 'results.yml')


def create_retriever(all_splits, embeddings):
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
    return retriever
