"""
    模型返回数据结构化 3种方式：
    1 Pydantic 对象  -底层实现：通过tool_calls()调用
    2 TypedDict 字典
    3 jsonschema 外部注入动态传参的场景 -底层实现：通过tool_calls()调用

    调用函数是：with_structured_output 但这个函数不支持推理模型的。需要看03_02
"""
from typing import List

from jsonschema import ValidationError
from langchain_core.runnables import RunnableSequence
from pydantic import BaseModel, Field
from typing_extensions import TypedDict, Annotated

from init_llm import deepseek_llm
import jsonschema

"""
    Pydantic
    所有类型都返回来了，属于强类型，推荐。
"""


# 对象方式 嵌套字对象
class Actor(BaseModel):
    name: str = Field(description='演员真实姓名')
    role: str = Field(description='演员角色名')


# 对象方式 Pydantic,强类型，所有属性都会返回
class Movie(BaseModel):
    title: str = Field(description='电影标题')
    year: int = Field(description='上映年份')
    director: str = Field(description='导演')
    rating: float = Field(description='评分（10分制）')
    actor_list: List[Actor] = Field(description='演员列表')


"""
    TypedDict
    返回来的数据有丢缺的 rating:'-'
"""


class ActorDict(TypedDict):
    name: Annotated[str, '姓名']
    role: Annotated[str, '角色']


class MovieDict(TypedDict):
    title: Annotated[str, '电影标题']
    year: Annotated[int, '上映年份']
    director: Annotated[str, '导演']
    rating: Annotated[float, '评分（10分制）']
    actor_list: Annotated[List[ActorDict], '演员列表']


"""
    jsonschema
    用在从外部过来的注入，返回类型：dict
"""

request_jsonschema = {
    "title": "MovieInfo",  # title是死的,value只能是英文
    "description": "包含电影标题、上映年份、导演和评分的电影对象",  # 描述要返回什么
    "properties": {  # 需要返回的数据
        "title": {"type": "string", "description": "电影标题"},
        "year": {"type": "integer", "description": "上映年份"},
        "director": {"type": "string", "description": "导演"},
        "rating": {"type": "number", "description": "评分（10分制）"},
        "cast": {"type": "array", "description": "演员列表",  # 嵌套一个列表
                 "items": {
                     "type": "object",
                     "properties": {
                         "name": {"type": "string", "description": "演员姓名"},
                         "role": {"type": "string", "description": "演员角色"}
                     },
                     "required": ["name", "role"]}
                 },
    },
    "required": ["title", "year", "director", "rating"]  # 表示必须要返回的内容,强制返回的字段，即使没有找到对应答案
}

from my_llm import deepseek_llm_local

if __name__ == '__main__':
    test_type: int = 3  # 1:Pydantic 2:typedict 3:jsonschema

    model_with_structured: RunnableSequence

    # 可以设置为true后，返回的数据为AIMessage全，全的中包含了：结构化的
    # deepseek_llm_local.with_structured_output(include_raw=True)

    if test_type == 1:
        model_with_structured = deepseek_llm_local.with_structured_output(Movie)
    elif test_type == 2:
        model_with_structured = deepseek_llm_local.with_structured_output(MovieDict)
    else:
        model_with_structured = deepseek_llm_local.with_structured_output(request_jsonschema)

    # 请求结果
    response = model_with_structured.invoke('帮我介绍一下电影：《泰坦尼克号》')

    # jsonschema类型，返回结果格式验证
    if test_type == 3:
        try:
            jsonschema.validate(instance=response, schema=request_jsonschema)
            print("校验通过")
        except ValidationError as e:
            print("校验失败：", e.message)

    print(f'结构类型：{type(response)}')
    print(response)
