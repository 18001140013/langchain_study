"""模型工具调用 LLM + Tools使用：
    1推理原理
    2多工具执行成功与失败案例
"""
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool

# 本地模型下：response.tool_calls 是个空数组，难道只能是线上吗？
# 确定了：是`deepseek-r1:7b` 原生没有训练工具调用格式
from init_llm import deepseek_llm_local, deepseek_llm

request_message = [HumanMessage(content="北京今天天气如何？")]


# 【1】定义工具
@tool
def get_weather(location: str) -> str:
    """获取指定位置的天气"""
    return f" {location}的天气是晴朗的。"


# 【2】绑定工具
model_with_tools = deepseek_llm.bind_tools([get_weather])

# 【3】模型调用
response: AIMessage = model_with_tools.invoke(request_message)
request_message.append(response)

#  [4] 工具手动调用
if response.tool_calls:
    for tool_call in response.tool_calls:  # [{dict}]
        if tool_call['name'] == 'get_weather':
            tool_call_result = get_weather.invoke(tool_call)
            request_message.append(tool_call_result)

final_response = model_with_tools.invoke(request_message)
request_message.append(final_response)

print(request_message)
print('--' * 60)
print(final_response)
# print(response.tool_calls)
# response.pretty_print()
