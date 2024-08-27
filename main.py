from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.llms.bedrock import Bedrock
import streamlit as st
from pypdf import PdfReader

prompt = st.chat_input("Say something")
file_upload = st.sidebar.file_uploader("Send a small PDFs")
clear_conversation = st.sidebar.button("🗑️ Clear conversation", type="primary")

model = Bedrock(model="mistral.mistral-7b-instruct-v0:2")

file_text = None
if file_upload is not None:
    with open("temp.pdf", "wb") as f:
        f.write(file_upload.getvalue())

    reader = PdfReader("temp.pdf")
    file_text = "\n\n".join([page.extract_text() for page in reader.pages])

if "messages" not in st.session_state:
    st.session_state.messages = []

if clear_conversation:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message.role.value):
        st.markdown(message.content)

if prompt is not None:
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append(ChatMessage(role=MessageRole.USER, content=prompt))

    messages = [
        ChatMessage(
            role=MessageRole.SYSTEM, content=f"Uploaded file content: {file_text}"
        ),
        *st.session_state.messages,
    ]

    resp = model.chat(messages)

    resp_text = resp.message.content
    print(resp_text)
    if resp_text.find("user:") != -1:
        resp_text = resp_text[:resp_text.find("user:")]

    with st.chat_message("assistant"):
        st.markdown(resp_text)

    st.session_state.messages.append(
        ChatMessage(role=MessageRole.ASSISTANT, content=resp_text)
    )
