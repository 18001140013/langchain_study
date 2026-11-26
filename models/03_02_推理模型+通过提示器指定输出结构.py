from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from env_util import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL

"""
    推理模型，返回的数据结构不能使用那三种，需要用parser解析器去解析模型返回的json数据成一个对象
"""
deepseek_reasoner_llm = init_chat_model(
    model="deepseek-reasoner",
    model_provider="deepseek",
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL,
)


# 1. 定义结构
class Movie(BaseModel):
    title: str = Field(description="电影标题")
    year: int = Field(description="上映年份")


# 2. 创建解析器和提示模板
parser = JsonOutputParser(pydantic_object=Movie)

prompt = ChatPromptTemplate.from_template("""
回答用户问题。
问题：{question}
你必须始终输出一个包含title(电影标题)和year(上映年份)的 JSON 对象。
""")

# 3. 创建链 prompt->deepseek_reasoner_llm->parser
chain = prompt | deepseek_reasoner_llm | parser

print(type(chain))  # <class 'langchain_core.runnables.base.RunnableSequence'>

# 4. 调用（返回字典）
response = chain.invoke({"question": "介绍电影《盗梦空间》"})
print(response)
