import streamlit as st

from app.ml_logic.preprocessing import preprocess_pdf_to_retriever, load_retriever
from app.interface.ui_logic import display_sidebar, display_intro, display_messages, is_openai_api_key_set, process_input

from app.ml_logic.model import agent_creation
from app.ml_logic.AgentTool import creation_Tools
from langchain.chat_models import ChatOpenAI

from app.params import *

import time

st.set_page_config(page_title="CoExpert", page_icon="logo.jpg")

start_time = time.time()
print(f"TARGET: {TARGET}")


def main():
    '''Main function to launch the app'''
    if len(st.session_state) == 0:

        print("Initializing OPENAI API KEY")
        st.session_state["OPENAI_API_KEY"] = OPENAI_API_KEY if TARGET == "local" \
            else st.secrets["OPENAI_API_KEY"]

        print("Initializing retriever")
        if not os.path.exists(CACHE_PATH_CHROMA) \
                or (len(os.listdir(CACHE_PATH_CHROMA)) == 0):
            retriever = preprocess_pdf_to_retriever(start_time)
        else:
            retriever = load_retriever(start_time)

        print("Initializing session variables")
        st.session_state["retriever"] = retriever
        st.session_state["messages"] = []
        st.session_state["web_agent"] = 0

        print("Agent & Tools creation")
        llm = ChatOpenAI(temperature=0,model='gpt-4-1106-preview')
        st.session_state['tools'] = creation_Tools(llm)
        st.session_state['agent'] = agent_creation(llm)

        print("---------- %s seconds ----------" % (time.time() - start_time))

        print("Session state initialized. Pending user input...")

    else:
        print("Session state already initialized")

    display_sidebar()

    display_intro()

    display_messages()
    st.divider()
    st.session_state["web_agent"] = st.toggle("Web Agent Research")
    st.text_input("Please enter your question:", key="user_input",
                  disabled=not is_openai_api_key_set(), on_change=process_input)


if __name__ == "__main__":
    main()
