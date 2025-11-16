import os
# 关闭LangSmith追踪
os.environ["LANGCHAIN_TRACING_V2"] = "false"
from dotenv import load_dotenv
load_dotenv()


from langchain_ollama import ChatOllama
from langchain_tavily import TavilySearch
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.messages import AIMessage

#
# model = ChatOpenAI(model="glm-4.6",
#                    api_key=os.getenv("ZHIPUAI_API_KEY"),
#                    base_url="https://open.bigmodel.cn/api/paas/v4/")
# model = ChatOllama(model="qwen2.5:3b")
# tavily = TavilySearch(max_results=3)

# system_prompt = "扮演一个既聪明又友好的人工智能聊天机器人"

def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt,provider):
    if provider == "Ollama":
        llm = ChatOllama(model=llm_id)
    elif provider == "ZHIPUAI":
        llm = ChatOpenAI(model=llm_id,
                         api_key=os.getenv("ZHIPUAI_API_KEY"),
                         base_url="https://open.bigmodel.cn/api/paas/v4/")
    tools = [TavilySearch(max_results=3)] if allow_search else []

    agent = create_agent(llm,
                         tools=tools,
                         system_prompt=system_prompt)
    # query = "告诉我最近的ai新闻"
    message = {"messages":query}
    res = agent.invoke(message)
    msg = res.get("messages")
    ai_messages = [message.content for message in msg if isinstance(message, AIMessage)]
    return ai_messages[-1]


# for m in agent.stream(message, stream_mode="values"):
#     m["messages"][-1].pretty_print()

# res = agent.invoke(message)
# msg = res.get("messages")
# ai_messages = [message.content for message in msg if isinstance(message, AIMessage)]
# print(ai_messages[-1])