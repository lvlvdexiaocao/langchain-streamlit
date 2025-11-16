from langchain_openai import ChatOpenAI
import os
# 关闭LangSmith追踪
os.environ["LANGCHAIN_TRACING_V2"] = "false"
from dotenv import load_dotenv
load_dotenv()

from vector_database import faiss_db
from langchain_core.prompts import ChatPromptTemplate
# 1.llm


model = ChatOpenAI(model="glm-4.5-flash",
                   api_key=os.getenv("ZHIPUAI_API_KEY"),
                   base_url="https://open.bigmodel.cn/api/paas/v4/")

# 2.retrieve docs
def retrieve_docs(query):
    return faiss_db.similarity_search(query)

def get_context(documents):
    context = "\n\n".join([doc.page_content for doc in documents])
    return context

# 3. qa
template = """
利用上下文中提供的信息来回答用户的问题。
如果你不知道答案，只需说不知道，不要试图编造答案。
不要提供超出给定上下文的内容。
问题：{question}
上下文：{context}
答案：
"""

def answer_query(documents, llm, query):
    context = get_context(documents)
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt|llm
    return chain.invoke({"question":query, "context":context})

question = "deepseek-v3的优于qwen2.5-72B百分之多少？"
retrieve = retrieve_docs(question)
# print("ai:", answer_query(documents=retrieve, llm=model, query=question))
