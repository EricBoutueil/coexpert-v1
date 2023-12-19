import streamlit as st
# from langchain.chains.question_answering import load_qa_chain
# from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor
from langchain import hub
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain.tools.render import render_text_description

## Modèle à query en direct (Query => Answer)
# def run_model(query):
#     '''Run the model'''
#     retriever = st.session_state["retriever"]
#     print(f'Using retriever: {retriever}')

#     # TODO: can get_relevant_documents receive query + st.session_state["messages"]
#     docs = retriever.get_relevant_documents(query)
#     print(f'Found {len(docs)} relevant documents')

#     # TODO: docs contains the source and page: use them for references ???
#     print(f'********** Docs contents and metadata: {docs}')

#     chain = load_qa_chain(ChatOpenAI(
#         temperature=0, openai_api_key=st.secrets["OPENAI_API_KEY"]), chain_type="stuff")
#     output = chain.run(input_documents=docs, question=query)
#     return output

## Création Agent (modèle de query ReAct/iteratif)
def agent_creation(llm):
    # Création de la liste des outils
    tool_names = ", ".join([tool.name for tool in st.session_state['tools']])

    prompt = hub.pull("hwchase17/react")
    prompt = prompt.partial(
    tool_names=tool_names,
    tools=render_text_description(st.session_state['tools']),
    )

    llm_with_stop = llm.bind(stop=["\nObservation"])

    # Définition du contexte associé à l'agent
    agent_context = """
        You're a doctor assistant from the pacemaker company Boston Scientific. \
        You're name is 'BS Assistant'. \
        If you find the answer in the documents provided by the company, you'll verify your answer with Google websearch tool. \
        Once you have verify your document answer with Google, you'll answer the question. \
        You're helping doctors to find the relevant information in the documents provided by the company \
        You WILL NOT answer questions that are not based on BOSTON SCIENTIFIC inputs, especially when you search on internet. \
        If you don't find the answer in the documents provided, you can search on Google but ONLY from BOSTON SCIENTIFIC inputs.
    """

    # Modification du prompt pour inclure le contexte
    modified_prompt = lambda x: agent_context + "\n" + x["input"]

    # Création de l'agent avec le contexte intégré
    agent = (
        {
            "input": modified_prompt,
            "agent_scratchpad": lambda x: format_log_to_str(x["intermediate_steps"]),
        }
        | prompt
        | llm_with_stop
        | ReActSingleInputOutputParser()
    )

    return agent

def agent_executor(query):
    agent_executor = AgentExecutor(agent=st.session_state['agent'], tools=st.session_state['tools'], verbose=True)

    resultat = agent_executor.invoke(
        {
            "input": query,
        }
    )

    return resultat['output']
