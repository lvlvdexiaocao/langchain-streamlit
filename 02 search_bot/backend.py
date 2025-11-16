from pydantic import BaseModel
from typing import List

from fastapi import FastAPI

from agent import get_response_from_ai_agent

# 1.设置pydantic模型
class RequestState(BaseModel):
    model_name:str
    model_provider:str
    system_prompt:str
    messages:List[str]
    allow_search:bool

# 2.agent从后端响应
ALLOWED_MODEL_NAMES = ["qwen2.5:3b", "glm-4.6", "glm-4.5-flash"]

app = FastAPI(title="search bot")

@app.post("/chat")
def chat_endpoint(request:RequestState):
    """
    使用LangGraph和搜索工具与聊天机器人交互的API端点。
    它会动态选择请求中指定的模型。
    """
    if request.model_name not in ALLOWED_MODEL_NAMES:
        return {"error":"模型名称无效。请选择有效的AI 模型。"}

    llm_id = request.model_name
    query = request.messages
    allow_search = request.allow_search
    system_prompt = request.system_prompt
    provider = request.model_provider

    response = get_response_from_ai_agent(llm_id, query, allow_search, system_prompt,provider)
    return response

# 3.运行
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9999)