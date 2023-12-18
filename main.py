import streamlit as st

from app.ml_logic.preprocessing import preprocess_pdf_to_retriever
from app.interface.ui_logic import display_messages, is_openai_api_key_set, process_input

from params import *


st.set_page_config(page_title="CoExpert")

print(f"TARGET: {TARGET}")
print(f'env: {LOCAL_OPENAI_API_KEY}')
print(f'secrets: {st.secrets["CLOUD_OPENAI_API_KEY"]}')


def main():
    '''Main function to launch the app'''
    if len(st.session_state) == 0:

        print("Initializing OPENAI API KEY")
        st.session_state["OPENAI_API_KEY"] = [
            LOCAL_OPENAI_API_KEY if TARGET == "local"
            else st.secrets["CLOUD_OPENAI_API_KEY"]][0]
        print(f"OPENAI API KEY: {st.session_state['OPENAI_API_KEY']}")

        print("Initializing retriever")
        retriever = preprocess_pdf_to_retriever()

        print("Initializing session variables")
        st.session_state["retriever"] = retriever
        st.session_state["messages"] = []

        print("Session state initialized. Pending user input...")

    else:
        print("Session state already initialized")

    st.header("Welcome to CoExpert")

    display_messages()
    st.text_input("Please enter your question:", key="user_input",
                  disabled=not is_openai_api_key_set(), on_change=process_input)

    st.divider()


if __name__ == "__main__":
    main()
