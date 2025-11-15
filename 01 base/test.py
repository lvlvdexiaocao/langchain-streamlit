from langchain_core.prompts import ChatPromptTemplate
import os
# 关闭LangSmith追踪
os.environ["LANGCHAIN_TRACING_V2"] = "false"

template = """
你是一个乐于助人的助手。请结合对话历史回答以下问题：
聊天历史：{chat_history}
用户问题：{user_question}
"""
prompt = ChatPromptTemplate.from_template(template)

print(prompt.invoke({"chat_history":chat_history,
                                    "user_question":user_question}))