

# 1.设置上传pdf函数
import streamlit as st
from rag_pipeline import answer_query, retrieve_docs, model

uploaded_file = st.file_uploader("上传PDF",
                                 type="pdf",
                                 accept_multiple_files=True)


# 2.设置聊体机器人框架QA
user_query = st.text_area("在此处比比。。", height=150, placeholder="快BIBI！")

ask_question = st.button("提交")

if ask_question:
    if uploaded_file:
        st.chat_message("user").write(user_query)

        # RAG pipeline
        retrieved_docs = retrieve_docs(user_query)
        # fixed_response = "这是一个rag响应"

        response = answer_query(documents=retrieved_docs, llm=model, query=user_query)
        st.chat_message("assistant").write(response.content)

    else:
        st.error("请先加载文档")