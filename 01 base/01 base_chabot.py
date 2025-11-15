
import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.messages import HumanMessage, AIMessage
import os
# 关闭LangSmith追踪
os.environ["LANGCHAIN_TRACING_V2"] = "false"


model = ChatOllama(model="qwen2.5:3b")

st.set_page_config(page_title="聊天机器人",page_icon="🤖")

st.title("Base_ChatBot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def get_response(user_query, chat_history):
    template = """
    你是一个乐于助人的助手。请结合对话历史回答以下问题：
    聊天历史：{chat_history}
    用户问题：{user_question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt|model|StrOutputParser()

    return chain.stream({
        "chat_history": chat_history,
        "user_question": user_query,
    })

for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)
    else:
        with st.chat_message("AI"):
            st.markdown(message.content)

user_query = st.chat_input("请输入")
if user_query is not None and user_query !="":
    st.session_state.chat_history.append(HumanMessage(user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        ai_response = st.write_stream(get_response(user_query, st.session_state.chat_history))


    st.session_state.chat_history.append(AIMessage(ai_response))