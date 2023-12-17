import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain


def run_model(query):
    '''Run the model'''
    retriever = st.session_state["retriever"]
    print(f'Using retriever: {retriever}')

    # TODO: can get_relevant_documents receive query + st.session_state["messages"]
    docs = retriever.get_relevant_documents(query)
    print(f'Found {len(docs)} relevant documents***')

    # TODO: docs contains the source and page: use them for references ???
    print(f'********** Docs contents and metadata: {docs}')

    chain = load_qa_chain(ChatOpenAI(
        temperature=0, openai_api_key=st.secrets["OPENAI_API_KEY"]), chain_type="stuff")
    output = chain.run(input_documents=docs, question=query)
    return output
