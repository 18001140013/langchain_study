"""
快速创建并启动一个agent
"""
from langchain.agents import create_agent
from langchain_core.tools import tool

from my_llm import deepseek_llm


@tool
def get_weather(location: str) -> str:
    """
    获取指定位置的天气信息
    :param location:
    :return:
    """
    return f'天气信息：{location} 的天气是寒冷的' # 这个结果会影响到模型


agent = create_agent(
    model=deepseek_llm,
    tools=[get_weather],
    system_prompt='你是一个天气助手，你可以帮助用户获取指定位置的天气信息',
)

request: dict = {"messages": [{'role': 'user', 'content': '北京的天气'}]}
resp = agent.invoke(request)
print(type(resp))  # 返回dict字典
print(resp)
