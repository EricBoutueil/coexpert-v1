from langchain.agents import load_tools
from langchain.tools import Tool
from langchain.utilities import GoogleSearchAPIWrapper


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

    # Ajoutdes outils créées dans la liste des outils de l'Agent
    tools = loaded_tools + [google_search_tool]

    return tools
