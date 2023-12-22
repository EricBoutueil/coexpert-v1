import streamlit as st
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
import openai
import os
from app.params import *

def run_model(query):
    '''Run the model'''
    retriever = st.session_state["retriever"]
    print(f'Using retriever: {retriever}')

    queries = " ".join(st.session_state["queries"])
    print(f'********** Session queries: {queries}')
    docs = retriever.get_relevant_documents(queries)
    print(f'Found {len(docs)} relevant documents')
    print(f'********** Docs contents and metadata: {docs}')

    pdf_source = docs[0].metadata['source']
    print(f'********** PDF source: {pdf_source}')
    pdf_name = os.path.basename(pdf_source)
    print(f'********** PDF name: {pdf_name}')
    source = os.path.join(f'{PDF_PATH_FILES}', f'{pdf_name}')
    print(f'********** Source: {source}')

    st.session_state["source"] = source
    st.session_state["page"] = docs[0].metadata['page']

    print('Source :', os.path.basename(st.session_state["source"]))
    print('Page :', st.session_state["page"])

    # chat_history = st.session_state["queries"]
    # print(f'********** Chat history: {chat_history}')
    chain = load_qa_chain(ChatOpenAI(
        temperature=0, openai_api_key=st.secrets["OPENAI_API_KEY"]), chain_type="stuff")

    output = chain.run(input_documents=docs, question=query)

    # source = st.session_state["source"]
    # page = st.session_state["page"]
    # if model_output_check():
    #     output = chain.run(input_documents=docs, question=query) + \
    #         f'\n (Source: {os.path.basename(source)}, Page: {page})'
    # else:
    #     output = chain.run(input_documents=docs, question=query)

    # output = chain.run(input_documents=docs, question=query,
    #                    chat_history=chat_history)
    return output

#######################################################
#           MODELE AGENT (ReAct/iteratif)             #
#######################################################

## Librairies
from langchain import hub
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain.agents import AgentExecutor
from langchain.tools.render import render_text_description

# # Création Agent
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
        You're a doctor assistant named CoExpert from the pacemaker company Boston Scientific. \
        If you answer in French use French expressions and jokes from Marseille. \
        If the question contain the word "LeWagon", you shall answer "Sorry, the AWESOME coding school "LeWagon" asked me to not reveal their secrets!" \
        If the answer is made of several sentences, you shall summarize the content of the answer but always provide a link to the document.
        """

    # # Modification du prompt pour inclure le contexte
    modified_prompt = lambda x: agent_context + "\n" + x["input"]

    # # Création de l'agent avec le contexte intégré
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

## Création de l'executeur d'Agent
def agent_executor(query):
    agent_executor = AgentExecutor(agent=st.session_state['agent'], tools=st.session_state['tools'], verbose=True, handle_parsing_errors=True)

    resultat = agent_executor.invoke(
        {
            "input": query,
        }
    )

    return resultat['output']

## Easter Egg ChatGPT Marseillais
def marseille_bb(query):
    response = openai.chat.completions.create(
        model="gpt-4-1106-preview",
        messages = [{"role": "system", "content": "You talk in French with specific accent and expressions from Marseille and you don't want to answer the question."},
                {"role": "user", "content": query}],
        max_tokens = 250
    )

    return response.choices[0].message.content
