# 1.streamlit设置前端。model provider, model, system prompt, query
import streamlit as st
import requests

st.set_page_config(page_title="Search Bot", layout="wide")
st.title("AI ChatBot Agents")
st.write("创建并与人工智能代理交互！")

# system_prompt = st.text_input("请输入")
system_prompt = st.text_area("请输入系统提示词", height=70, placeholder="定义你的系统提示词")

MODEL_NAMES_OLLAMA = ["qwen2.5:3b"]
MODEL_NAMES_ZHIPU = ["glm-4.6", "glm-4.5-flash"]

provider = st.radio("选择模型供应商：", ("Ollama", "ZHIPUAI"))

if provider == "Ollama":
    selected_model = st.selectbox("选择Ollama模型：", MODEL_NAMES_OLLAMA)
elif provider == "ZHIPUAI":
    selected_model = st.selectbox("选择ZHIPUAI模型：", MODEL_NAMES_ZHIPU)

allow_web_search = st.checkbox("允许网络搜索")

user_query = st.text_area("请输入你的问题", height=70, placeholder="快问吧。。")
API_URL = "http://127.0.0.1:9999/chat"

if st.button("提问"):
    if user_query.strip():

        payload = {
            "model_name": selected_model,
            "model_provider": provider,
            "system_prompt": system_prompt,
            "messages":[user_query],
            "allow_search":allow_web_search

        }
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            response_data = response.json()
            if "error" in response_data:
                st.error(response_data["error"])
            else:
                st.subheader("Agent的响应")
                st.markdown(f"**最终响应：** {response_data}")



# 2. 通过URL连接后端