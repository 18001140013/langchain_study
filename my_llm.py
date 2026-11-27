"""
使用model class方式：
创建各平台模型 LLM
"""
from langchain_deepseek import ChatDeepSeek
from langchain_ollama import ChatOllama

from env_util import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL

# deepseek线上模型
deepseek_llm = ChatDeepSeek(
    model_name='deepseek-flash',
    api_key=DEEPSEEK_API_KEY,
    api_base=DEEPSEEK_BASE_URL,
)
# deepseek线下模型 用ollama启动
deepseek_llm_local = ChatOllama(model="deepseek-r1:7b", base_url="http://localhost:11434")
# 通义千问线下模型
qwen_llm_local = ChatOllama(model="qwen3:8b", base_url="http://localhost:11434")

# 测试对话：
if __name__ == '__main__':
    request: dict = {"messages": [{'role': 'user', 'content': '北京的天气'}]}
    resp = deepseek_llm.invoke('介绍一下您自己？')
    print(type(resp))  # <class 'langchain_core.messages.ai.AIMessage'>
    print(resp)
