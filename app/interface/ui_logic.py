import streamlit as st
from streamlit_chat import message

from app.ml_logic.model import run_model
from app.ml_logic.model import agent_executor, marseille_bb

import codecs
import os


def display_sidebar():
    st.sidebar.image('logo-500px.png', width=200)
    st.sidebar.title(':blue[CoExpert creators:]')
    st.sidebar.write("""
        ### Boutueil Eric [LinkedIn](https://www.linkedin.com/in/ericboutueil/)
        ### Sagols Thomas [LinkedIn](https://www.linkedin.com/in/thomas-sagols-15439a13/)
        ### Janer Denis [LinkedIn](https://www.linkedin.com/in/denis-janer-2430b47/)
         """)


def display_intro():
    col1, col2 = st.columns([1, 4])
    col1.text('')
    col1.image('logo-100px.png', width=100)
    col2.header(":blue[Welcome, I'm CoExpert]")
    col2.subheader(
        "My current expertise: BSC cardiac devices")


def display_messages():
    '''Display discussion'''
    for i, (msg, is_user) in enumerate(st.session_state["messages"]):
        if is_user:
            message(msg, is_user=is_user, key=str(i))
        else:
            message(msg, is_user=is_user, key=str(i),
                    avatar_style="bottts", seed="l")
    st.session_state["thinking_spinner"] = st.empty()


def model_output_check():
    last_output = st.session_state["last_output"]
    # return "CRT" in last_output or "ICD" in last_output or "model" in last_output
    check = any(keyword in last_output for keyword in ["CRT", "ICD", "model", "dimension"]) and not any(
        keyword in last_output for keyword in ["I'm sorry", "does not provide"])
    print(f'*Model output check*: {check}')
    return check


def displayPDF():
    print(f'*Show pdf state*: {st.session_state["show_pdf"]}')
    # print(f'model_output_check: {model_output_check()}')
    if st.session_state["show_pdf"] and model_output_check():
        # if model_output_check():
        print("*DisplayPDF - Start*")
        source = st.session_state["source"]
        # page = st.session_state["page"]
        datafile = open(source, 'rb')
        pdfdatab = datafile.read()  # this is binary data
        datafile.close()

        # Convert to utf-8
        b64PDF = codecs.encode(pdfdatab, 'base64')
        base64_pdf = b64PDF.decode('utf-8')

        # Embed PDF in HTML
        pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="300" type="application/pdf"></iframe>'

        # Display file
        st.markdown(pdf_display, unsafe_allow_html=True)
        print("*DisplayPDF - End*")


def display_chat_input():
    col1, col2 = st.columns([1, 1])
    with col1:
        st.session_state["web_agent"] = st.toggle("Web Agent Research")
    with col2:
        st.session_state["show_pdf"] = st.toggle("Show Pdf (Firefox)")
    print(f'Show pdf state: {st.session_state["show_pdf"]}')
    st.chat_input(placeholder="Your question", key="user_input",
                  disabled=not is_openai_api_key_set(), on_submit=process_input)


def process_input():
    '''Process user input'''
    if st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
        print(f'User input: {st.session_state["user_input"]}')
        query = st.session_state["user_input"].strip()
        print(f'Query: {query}')
        st.session_state["queries"].append(query)

        if st.session_state["web_agent"] == 0:
            with st.session_state["thinking_spinner"], st.spinner(f"Thinking"):
                model_output = run_model(query)
            st.session_state["last_output"] = model_output
        elif st.session_state["web_agent"] == 1:
            with st.session_state["thinking_spinner"], st.spinner(f"Thinking"):
                if query.lower().find('french') == -1:
                    model_output = agent_executor(query)
                else:
                    model_output = marseille_bb(query)

        source = st.session_state["source"]
        page = st.session_state["page"]
        if model_output_check():
            output = model_output + \
                f'\n (Source: {os.path.basename(source)}, Page: {page})'
        else:
            output = model_output

        st.session_state["messages"].append((query, True))
        st.session_state["messages"].append((output, False))
        print(f'********** Session messages: {st.session_state["messages"]}')


def is_openai_api_key_set() -> bool:
    return len(st.session_state["OPENAI_API_KEY"]) > 0
