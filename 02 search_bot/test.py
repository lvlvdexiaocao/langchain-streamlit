from langchain_tavily import TavilySearch
import os
# 关闭LangSmith追踪
os.environ["LANGCHAIN_TRACING_V2"] = "false"
from dotenv import load_dotenv
load_dotenv()

from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

# model = ChatOllama(model="qwen2.5:3b")
# tavily = TavilySearch(max_results=3)


model = ChatOpenAI(model="glm-4.6",
                   api_key=os.getenv("ZHIPUAI_API_KEY"),
                   base_url="https://open.bigmodel.cn/api/paas/v4/")
res = model.invoke("你好")
print(res)
#
# agent = create_agent(model, [tavily])
# user_input = "langchain是什么"
# for m in agent.stream({"messages":user_input}, stream_mode="values"):
#     m["messages"][-1].pretty_print()


