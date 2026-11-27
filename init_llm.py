"""
使用 init_chat_model 方式：
创建各平台模型 LLM
"""
from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel

from env_util import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL

# deepseek线上模型
deepseek_llm: BaseChatModel = init_chat_model(
    model="deepseek-chat", model_provider="deepseek",
    api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL, )

# deepseek本地模型 使用ollama部署与启动
deepseek_llm_local = init_chat_model(
    model="deepseek-r1:7b",
    model_provider="ollama",
    base_url="http://localhost:11434",
    temperature=0.7
)

# 通义千问线下模型
qwen_llm_local = init_chat_model(
    model="qwen3:8b",
    model_provider="ollama",
    base_url="http://localhost:11434",
)

if __name__ == "__main__":
    # resp = deepseek_llm.invoke('介绍一下您自己？')
    # print(type(resp))  # <class 'langchain_core.messages.ai.AIMessage'>
    # print(resp)

    resp = deepseek_llm_local.invoke('帮我讲个儿童寓言故事？字数限制在100字内')
    print(type(resp))  # <class 'langchain_core.messages.ai.AIMessage'>
    print(resp)
