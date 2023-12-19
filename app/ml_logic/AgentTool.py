from langchain.agents import load_tools
from langchain.tools import Tool
from langchain.utilities import GoogleSearchAPIWrapper
import streamlit as st

## Fonction search doc from retriever
def search_documents(query):
    retriever = st.session_state["retriever"]
    # Utilisez as_retriever pour trouver les documents pertinents
    docs = retriever.get_relevant_documents(query)

    return docs


## Création du document tool Langchain
def creation_Tools(llm):
    # Tool's import from langchain (Here maths, but can be several others)
    loaded_tools = load_tools(["llm-math"], llm=llm)

    # Création de l'outil de recherche Google
    search = GoogleSearchAPIWrapper()
    google_search_tool = Tool(
        name="Google Search",
        description="""
        Search on internet for the answer.
        """,
        func=search.run,
    )

    # Création de l'outil de recherche de documents
    document_search_tool = Tool(
        name="Document Search",
        description="""
        Search for answers in a set of indexed documents. \
        When using the document search tool, you shall always specify clearly each step of your reasoning. \
        If the question requires several steps of reasoning you specify it in your question.
        """,
        func=search_documents
    )

    # Ajoutdes outils créées dans la liste des outils de l'Agent
    tools = loaded_tools + [google_search_tool] + [document_search_tool]

    return tools
