"""模型工具调用 LLM + Tools使用：
    调用步骤，如何使用。
"""
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool

# 本地模型下：response.tool_calls 是个空数组，难道只能是线上吗？
# 确定了：是`deepseek-r1:7b` 原生没有训练工具调用格式
from init_llm import deepseek_llm_local, deepseek_llm

request_message = []
request_tools: dict = {}


# 【1】定义工具
@tool
def get_stock_price(company: str, timeframe: str = "today") -> str:
    """获取指定公司的股票价格信息

    Args:
        company: 公司名称（如：苹果公司, 微软公司, 谷歌公司）
        timeframe: 时间范围（today-今日, week-本周, month-本月）
    """
    # 模拟股票数据
    mock_data = {
        "苹果公司": {"today": 185.20, "week": 183.50, "month": 180.75},
        "微软公司": {"today": 415.86, "week": 412.30, "month": 405.42},
        "谷歌公司": {"today": 15.42, "week": 15.20, "month": 14.85}
    }

    if company in mock_data:
        price = mock_data[company].get(timeframe, "未知时间范围")
        return f"{company} {timeframe}价格: {price}美元"
    else:
        return f"未找到股票代码 {company} 的数据"


@tool
def search_news(company: str) -> str:
    """搜索指定公司的财经新闻
    Args: company: 公司名称
    Return: 公司的财经新闻，每个新闻占一行
    """

    # 模拟新闻数据
    mock_news = {
        "苹果公司": ["苹果发布新款iPhone，股价上涨3%", "苹果与欧盟达成反垄断和解协议", "苹果将在印度扩大生产规模"],
        "微软公司": ["微软Azure云业务季度增长超预期", "微软完成对Nuance的收购", "微软推出新一代AI助手Copilot"],
        "谷歌公司": ["谷歌发布新AI模型，性能提升20%", "谷歌与OpenAI合作，开发新的AI助手", "谷歌在欧洲展开AI研究项目"]
    }
    news_list = mock_news.get(company, [f"未找到{company}的相关新闻"])
    return "\n".join(news_list)


# 工具方法
request_tools['search_news'] = search_news
request_tools['get_stock_price'] = get_stock_price

# 请求问题
human_message = HumanMessage(content="苹果公司今天的股价是多少？最近有什么新闻？")
# human_message = HumanMessage(content="比较一下微软和苹果的股价")
# human_message = HumanMessage(content="腾讯最近有什么重大新闻？")
# human_message = HumanMessage(content="海水为什么是咸的？")
request_message.append(human_message)

# 【2】绑定工具
model_with_tools = deepseek_llm.bind_tools([get_stock_price, search_news])

#  循环完成：【3】模型调用 [4] 工具手动调用
while True:
    response: AIMessage = model_with_tools.invoke(request_message)
    request_message.append(response)

    if response.tool_calls:  # 一次行执行返回的所有工具函数 function calling
        for tool_call in response.tool_calls:  # [{dict}]
            tool_call_name = tool_call['name']
            if tool_call_name in request_tools:
                request_message.append(request_tools[tool_call_name].invoke(tool_call))
    else:
        break

print(request_message)
print('--' * 60)
print(request_message[-1].content)
# print(response.tool_calls)
# response.pretty_print()
