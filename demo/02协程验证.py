import asyncio
import threading
from threading import current_thread


# 任务函数
async def task(name, delay):
    for i in range(3):
        print(f'------------------执行：{name} - {i}')
        await asyncio.sleep(delay)
        # print(f'task 当前线程： {current_thread().name}') # # 输出：'CoroutineThread'
    return f'task任务回参-{name}'


"""
    使用异步完成多任务并发： task：执行3个1s时间等待，2个task 如果用同步总时长为：3*2=6s, 用协程异步任务完成：3s。
    多并发通过异步任务完成：发挥了机器性能，提高了完成速度。
    
    多协程完成并发。同一个线程下，多个任务交替切换完成执行。适合IO密集（网络请求、本地文件，输入输出的）。
    多线程完成多并发。多线程共用一个cpu资源 共享一个GIL锁，交替切换完成执行。
    多协程完成多并发，也可完成多并行。多个协程就分配多个cpu资源，多个GIL锁，并行完成任务，比较适合cpu密集（计算）。
"""


# 协程入口
async def main():
    print(f'main1 当前线程： {current_thread().name}')  # 输出：'CoroutineThread'

    """
         【1】这个是异步写法: 会在异步方法中优先执行底部代码在启动异步
        ，如果半路有任意一个await 都会优先把异步执行完再向下执行。
    """
    task1 = asyncio.create_task(task('1', 1))
    task2 = asyncio.create_task(task('2', 1))

    """
        这个是异步写法:会通知启动task1 task2,这两个异步交替执行
        下方await 让出了main资源 给到了异步task 然后再获取异步结果
    """
    print(await task1)
    print(await task2)
    # print(await asyncio.gather(task1, task2))

    """
        【2】这个是同步写法: 先执行完3 再开始执行4，await就是等待一个任务完成
    """
    # await task('3', 1)
    # await task('4', 1)

    """
        【3】休眠3s,释放了main函数资源，让给了 task1 task2，此时：2个异步任务task会交替切换执行 
            待获取到资源后再执行下方打印
    """
    # print(f'------------------main 休眠1s {await asyncio.sleep(3)}')

    print(f'main2 当前线程： {current_thread().name}')  # 输出：'CoroutineThread'


#  测试
if __name__ == '__main__':
    def coroutine_task():
        """
        【协程会在哪个线程中执行？】asyncio.run：阻塞函数，默认会在mainThread线程中执行。
        :return:
        """
        asyncio.run(main())  # run为阻塞函数


    """
        将协程任务单独放在一个线程中，与MainThread区分开 达到线程异步，会优先打印下方
    """
    threading.Thread(target=coroutine_task, name='CoroutineThread').start()

    print(f'test 当前线程： {current_thread().name}')  # 输出：'MainThread'
