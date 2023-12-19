
from langchain.agents import load_tools
from langchain.tools import Tool
from langchain.utilities import GoogleSearchAPIWrapper
import streamlit as st

## Fonction search doc from retriever
def search_documents(question):
    retriever = st.session_state["retriever"]
    # Utilisez as_retriever pour trouver les documents pertinents
    docs = retriever.get_relevant_documents(question)

    return docs


## Création du document tool Langchain
def creation_Tools(llm):
    # Tool's import from langchain (Here maths, but can be several others)
    loaded_tools = load_tools(["llm-math"], llm=llm)

    # Création de l'outil de recherche Google
    search = GoogleSearchAPIWrapper()
    google_search_tool = Tool(
        name="Google Search",
        description="Search on the web ONLY IF you didn't find the answer in the documents or if you need to confirm what you found in the documents.",
        func=search.run,
    )

    # Création de l'outil de recherche de documents
    document_search_tool = Tool(
        name="Document Search",
        description="Search IN PRIORITY for answers in a set of indexed documents.",
        func=search_documents
    )

    # Ajoutdes outils créées dans la liste des outils de l'Agent
    tools = loaded_tools + [google_search_tool] + [document_search_tool]

    return tools
