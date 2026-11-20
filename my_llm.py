"""
创建各类的模型 LLM
"""
from langchain_deepseek import ChatDeepSeek

from env_util import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL

# deepseek模型
deepseek_llm = ChatDeepSeek(
    model_name='deepseek-flash',
    api_key=DEEPSEEK_API_KEY,
    api_base=DEEPSEEK_BASE_URL,
)
