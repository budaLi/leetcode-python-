# @Time    : 2019/9/19 14:54
# @Author  : Libuda
# @FileName: loop_test.py
# @Software: PyCharm

# 高并发编程 三个要素
# 事件循环
#  回调  驱动生成器 驱动协程
#  epoll(io多路复用)
# asyncio 是python用于解决IO异步编程的一整套解决方案
# 使用 asyncio 的框架包括tornordo gevent twisted 而scrapy django channels 主要使用了twisted作为底层

import time
import asyncio
from functools import partial  # 将函数和参数重新组合成一个函数


async def get_html(url):
    print("start get url")

    # 在这里要注意的是 不能使用time.sleep 这种传统的阻塞方式
    # 必须使用await等待完成
    await asyncio.sleep(2)
    return "libuda"


def mycallback(url, future):
    print(url)
    print(future)
    # 要注意 当回调函数中需要传参数时 参数必须放在前面
    print("send email")


if __name__ == "__main__":
    # start_time = time.time()
    #
    # #协程必须搭配事件循环才能使用
    # loop = asyncio.get_event_loop()
    #
    # # get_future = asyncio.ensure_future(get_html("www.libuda.com"))
    #
    # task = loop.create_task(get_html("www.libuda.com"))
    #
    # #使用这种方式可以在上面函数结束后加入回调函数
    # #在这里要注意的是回调函数必须接收一个future参数 且当该函数需要传递参数时需要借助其他库
    # task.add_done_callback(partial(mycallback,"libudalalalal"))
    # #ssyncio.wait 可以接收一个可迭代的对象 等待所有任务结束后进行下一步
    # loop.run_until_complete(task)
    # print(task.result())
    # print("time",time.time()-start_time)

    # ____________________________________________________________________________________

    # gather比await更加高级
    start_time = time.time()
    loop = asyncio.get_event_loop()
    group1 = [get_html("libuda") for i in range(10)]
    group2 = [get_html("qidudu") for i in range(10)]

    group1 = asyncio.gather(*group1)
    group2 = asyncio.gather(*group2)

    # gather可以将任务分组 还可以取消任务
    # group1.cancel()
    loop.run_until_complete(asyncio.gather(group1, group2))
    print("time", time.time() - start_time)
