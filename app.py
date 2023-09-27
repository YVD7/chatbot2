import os
import openai
import streamlit as st
from streamlit_chat import message
from embedchain import App #, OpenSourceApp 
# from apikey import OPENAI_API_KEY


# Create a streamlit app title and description
st.title("Online Resoruce Chatbot:books:")
st.write("Enter multiple URL links and ask queistons to the embedded data.")

# initialize the openresourceApp instance
# zuck_bot = OpenSourceApp()
# os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
openai.api_key = st.secrets['OPENAI_API_KEY']
zuck_bot = App()


# get user input for URLs
num_links = st.number_input("Enter the numbers of the URLs:", min_value=1, value=1, step=1)

urls_inputs = []

for i in range(num_links):
    url = st.text_input(f"Enter URL {i+1}:", key=f'url_{i}')
    urls_inputs.append(url)

# add urls to the opensourceApp instance
for url in urls_inputs:
    if url:
        zuck_bot.add("web_page", url)

# conversation chat functions
def conversations_chat(querry):
    result = zuck_bot.query(querry)
    st.session_state['history'].append((querry, result))
    return result

def initialize_session_state():
    if "history" not in st.session_state:
        st.session_state['history'] = []

    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hello! Ask me anything about"]

    if "past" not in st.session_state:
        st.session_state['past'] = ["Hey!"]

def display_chat_history():
    reply_container = st.container()
    container = st.container()

    with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_input("Question:", placeholder="Ask me about resources", key="input")
            submit_button = st.form_submit_button(label='send')

        if submit_button and user_input:
            output = conversations_chat(user_input)
            st.session_state["past"].append(user_input)
            st.session_state['generated'].append(output)

    if st.session_state['generated']:
        with reply_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state['past'][i], is_user=True, key=str(i)+"_user", avatar_style="thumbs")
                message(st.session_state['generated'][i], key=str(i), avatar_style="fun-emoji")

# initialize the session_state
initialize_session_state()

# Display the chat history
display_chat_history()
