from llama_index.core.llms import ChatMessage
from llama_index.llms.bedrock import Bedrock
import streamlit as st
from pypdf import PdfReader

prompt = st.chat_input("Say something")
file_upload = st.sidebar.file_uploader("Send me a file")

if prompt is not None:
    user_message = st.chat_message("user")
    user_message.write(prompt)

    file_text = ""
    if file_upload is not None:

        with open("temp.pdf", "wb") as f:
            f.write(file_upload.getvalue())

        reader = PdfReader("temp.pdf")
        page = reader.pages[0]
        file_text = page.extract_text()
    messages = [
        ChatMessage(
            role="system", content="You are a pirate with a colorful personality"
        ),
        ChatMessage(role="user", content=f"{file_text}\n\n{prompt}"),
    ]

    resp = Bedrock(
        model="mistral.mistral-7b-instruct-v0:2"
    ).chat(messages)

    bot_message = st.chat_message("assistant")
    bot_message.write(resp.message.content)
