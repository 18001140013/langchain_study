from langchain.agents import create_agent
from langchain_core.tools import tool

from init_llm import qwen_llm_local, deepseek_llm_local

"""搭建一个智能体
    扩展2个tool,实现对指定公司的最新新闻、股价查询
    deepseek-r1:7b
    
    【Agent】核心工作原理：遵循ReAct框架（Reasoning+Acting）
    推理+行动 这个过程涉及到：模型、工具、记忆、中间件等核心组件。
"""


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


agent = create_agent(
    model=qwen_llm_local,
    tools=[get_stock_price, search_news],
    system_prompt='你是一个查询公司信息的助手，你可以帮助用户获取指定公司的信息如：股票价格、最新新闻等',
)

request: dict = {"messages": [{'role': 'user', 'content': '苹果公司今天的股价是多少？最近有什么新闻？'}]}
resp = agent.invoke(request)
print(type(resp))  # 返回dict字典
print(resp['messages'][-1].content)
