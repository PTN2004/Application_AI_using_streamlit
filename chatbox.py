import streamlit as st
from hugchat import hugchat
from hugchat.login import Login


def generate_response(prompt_input, email, password):
    sign = Login(email, password)
    cookies = sign.login()

    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    return chatbot.chat(prompt_input)


st.title("Simple ChatBot")

with st.sidebar:
    st.title("Login Hugchat")
    hf_email = st.text_input('Enter Email: ')
    hf_password = st.text_input('Enter Password: ', type='password')

    if not (hf_email and hf_password):
        st.warning("Please enter your account !")
    else:
        st.success("Proceed to entering your prompt message !")
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant",
                                  "content": "How may I help you ?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        print(message)
        st.write(message["content"])

if prompt := st.chat_input(disabled=not (hf_email and hf_password)):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            print(hf_email)
            print(hf_password)
            response = generate_response(prompt, hf_email, hf_password)
            print(response)
            st.write(response)
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)
    print(st.session_state.messages)
