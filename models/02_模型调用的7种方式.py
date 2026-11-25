"""
模型的各个调用函数与返回类型:

    invoke2种：
        # invoke    -> AIMessage -> 消息对象
        # ainvoke   -> asyncio.task -> 异步任务
    流式2种：
        # stream    -> Iterable -> generator -> 生成器
        # astream   -> AsyncIterator -> async_generator -> 异步生成器
    批量3种：
        # batch     -> list -> 列表
        # abatch    -> list -> 列表
        # batch_as_completed -> generator -> 生成器

"""

import asyncio
from collections.abc import Iterator, AsyncIterator

from langchain_core.messages import HumanMessage
from langchain_core.runnables.utils import Output

from my_llm import deepseek_llm_local


# 同步[invoke]调用模型3种格式：
def invoke():
    """
        dict格式：
        send_data = [
            {'role': 'system', 'content': ''},  # SystemMessage(content:"")
            {'role': 'user', 'content': ''},  # HumanMessage(content:"")
            {'role': 'assistant', 'content': ''},  # AIMessage(content:"")
            {'role': 'tool', 'content': ''},  # ToolMessage(content:"")
        ]
    """
    print(f'invoke1: {deepseek_llm_local.invoke('介绍一下自己')}')
    print(f'invoke2: {deepseek_llm_local.invoke([HumanMessage(content='介绍一下自己')])}')


# 同步[流式]调用模型
def stream():
    print('程序开始...')
    stream_resp: Iterator = deepseek_llm_local.stream('介绍一下自己')

    print('stream_resp type:', type(stream_resp))  # 生成器：generator

    for chunk in stream_resp:
        if hasattr(chunk, 'content'):
            print(chunk.content, end='', flush=True)  # flush=True 立刻内容刷新到屏幕上
    print('程序结束...')


# 同步[批量]调用模型
def batch():
    print('程序开始...')
    """
    batch()特点是等待所有请求处理完毕，按原始输入顺序返回结果列表。
    当输入列表很大或单个模型调用耗时差异显著时.
    """
    batch_resp: list[Output] = deepseek_llm_local.batch(
        ["为什么鹦鹉的羽毛是彩色的？", "飞机是如何飞行的？", "什么是量子计算？"])
    print('batch_resp type:', type(batch_resp))  # 列表：list
    for chunk in batch_resp:
        if hasattr(chunk, 'content'):
            print(chunk.content, end='', flush=True)  # flush=True 立刻内容刷新到屏幕上
    print('程序结束...')


# 同步[批量]调用模型 一条完成即可返回
def batch_as_completed():
    print('程序开始...')
    """
    batch_as_completed()允许应用在收到第一个结果后立即开始后续处理，而不必等待最慢的那个请求，也就是说
    batch_as_completed() 每个请求完成后立即 yield 结果，结果可能乱序，但包含索引信息。
    """
    responses: Iterator[tuple[int, Output | Exception]] = deepseek_llm_local.batch_as_completed(
        ["为什么鹦鹉的羽毛是彩色的？", "飞机是如何飞行的？", "什么是量子计算？"])

    print('batch_resp type:', type(responses))  # 生成器：generator

    for response in responses:
        # response 包含结果及其在原始列表中的索引
        print(f"第 {response[0]} 个问题回答完毕: {response[1].content}")

    print('程序开始...')


# 异步[invoke]调用模型
async def async_invoke():
    print('程序开始...')
    task1 = asyncio.create_task(deepseek_llm_local.ainvoke('介绍一下自己'))

    print('task1 type:', type(task1))  # 异步任务：_asyncio.Task

    print('程序结束...')

    print('异步获取:', await task1)


# 异步[流式]调用模型
async def async_stream():
    """演示异步调用的非阻塞特性"""
    print("=== 演示：astream 的异步（非阻塞）效果 ===")
    print("程序开始...")

    # 1. 发起异步流式请求，但不立即处理结果
    print(">>> 发起异步流式调用 (astream)...")
    stream_resp: AsyncIterator = deepseek_llm_local.astream('介绍一下自己')

    print('stream_resp type:', type(stream_resp))  # 异步生成器：async_generator

    # 2. 在等待流式响应的同时，执行其他任务
    for i in range(3):
        # 等待1s
        await asyncio.sleep(1)
        print(f">>> 正在执行第{i + 1}个任务... ")

    # 3. 现在开始处理流式结果
    print(">>> 其他任务已完成，开始处理流式结果...")

    print(">>> 流式输出: ", end="", flush=True)
    async for chunk in stream_resp:
        if hasattr(chunk, 'content'):
            print(chunk.content, end='', flush=True)  # flush=True 立刻内容刷新到屏幕上

    print(">>> 流式输出结束\n")


# 异步[批量]调用模型
async def async_batch():
    """演示单个异步调用的非阻塞特性"""
    print("=== 演示：abatch 的异步（非阻塞）效果 ===")

    print("程序开始...")

    # 准备批量输入（即使是单个输入，也用列表形式）
    questions = ["用一句话说明深度学习与传统机器学习的区别"]

    # 1. 发起异步批量请求
    print(">>> 发起异步批量调用 (abatch)...")
    batch_resp = deepseek_llm_local.abatch(questions)

    # 2. 在等待批量处理的同时，执行其他任务
    print(">>> 批量请求已发送，程序无需等待，继续执行...")
    for i in range(3):
        # 等待1s
        await asyncio.sleep(1)
        print(f">>> 正在执行第{i + 1}个任务... ")

    # 3. 等待批量处理结果
    print(">>> 其他任务已完成，现在等待批量处理结果...")
    responses = await batch_resp

    print('responses type:', type(responses))  # 列表：list

    for response in responses:
        print(f">>> 批量响应: {response.content}")


if __name__ == '__main__':
    # invoke()
    # stream()
    # batch()
    # batch_as_completed()
    asyncio.run(async_invoke())
    # asyncio.run(async_stream())
    # asyncio.run(async_batch())
