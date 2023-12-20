import streamlit as st
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI

## Modèle à query en direct (Query => Answer)
def run_model(query):
    '''Run the model'''
    retriever = st.session_state["retriever"]
    print(f'Using retriever: {retriever}')

    # TODO: can get_relevant_documents receive query + st.session_state["messages"]
    docs = retriever.get_relevant_documents(query)
    print(f'Found {len(docs)} relevant documents')

    # TODO: docs contains the source and page: use them for references ???
    print(f'********** Docs contents and metadata: {docs}')

    chain = load_qa_chain(ChatOpenAI(
        temperature=0, openai_api_key=st.secrets["OPENAI_API_KEY"]), chain_type="stuff")
    output = chain.run(input_documents=docs, question=query)
    return output

#######################################################
#           MODELE AGENT (ReAct/iteratif)             #
#######################################################

## Librairies
# from langchain import hub
# from langchain.agents.format_scratchpad import format_log_to_str
# from langchain.agents.output_parsers import ReActSingleInputOutputParser
# from langchain.agents import AgentExecutor
# from langchain.tools.render import render_text_description

## Création Agent
# def agent_creation(llm):
#     # Création de la liste des outils
#     tool_names = ", ".join([tool.name for tool in st.session_state['tools']])

#     prompt = hub.pull("hwchase17/react")
#     prompt = prompt.partial(
#     tool_names=tool_names,
#     tools=render_text_description(st.session_state['tools']),
#     )

#     llm_with_stop = llm.bind(stop=["\nObservation"])

#     # Définition du contexte associé à l'agent
#     agent_context = """
#         If the question contain the word "LeWagon", you shall answer "Sorry, the AWESOME coding school "LeWagon" asked me to not reveal their secrets!"  \
#         Always finish you're answer by "(Tool used: Document search)" or "(Tool used: Internet)" or "(Tool used: Calculator)" or nothing if it is about "LeWagon" \
#         You're a doctor assistant from the pacemaker company Boston Scientific. \
#         You're name is 'CoExpert'. \
#         You shall NEVER ONLY SAY: "I found information on [...] in the documents", always explain/summarize the content you found or say you don't know \
#         If the answer is made of several sentences, you shall summarize the content of the answer but always provide a link to the document. \
#         You're helping doctors to find the relevant information in the documents provided by the company
#     """

#     # Modification du prompt pour inclure le contexte
#     modified_prompt = lambda x: agent_context + "\n" + x["input"]

#     # Création de l'agent avec le contexte intégré
#     agent = (
#         {
#             "input": modified_prompt,
#             "agent_scratchpad": lambda x: format_log_to_str(x["intermediate_steps"]),
#         }
#         | prompt
#         | llm_with_stop
#         | ReActSingleInputOutputParser()
#     )

#     return agent

## Création de l'executeur d'Agent
# def agent_executor(query):
#     agent_executor = AgentExecutor(agent=st.session_state['agent'], tools=st.session_state['tools'], verbose=True, handle_parsing_errors=True)

#     resultat = agent_executor.invoke(
#         {
#             "input": query,
#         }
#     )

#     return resultat['output']
