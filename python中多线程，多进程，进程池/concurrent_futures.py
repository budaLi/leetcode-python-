# @Time    : 2019/9/27 8:13
# @Author  : Libuda
# @FileName: concurrent_futures.py
# @Software: PyCharm

# 提供线程控制 线程状态及返回值
# 当线程完成之后主线程可以知道其状态及返回结果
# 可以让多线程和多进程编码接口一致
from  concurrent.futures import ThreadPoolExecutor, as_completed, wait, FIRST_COMPLETED
import time


def get_html(times):
    time.sleep(times)
    print("get page {} ".format(times))
    return times


executor = ThreadPoolExecutor(max_workers=2)
# 通过submit函数将执行的函数提交到线程池中

# 1.一个一个提交任务
# task1 = executor.submit(get_html,(2)) #这里参数并不能使用(2,)
# task2 = executor.submit(get_html,(3))
#
# #判断任务是否完成
# print(task1.done())
# print(task2.done())
#
# #通过cancel可以取消任务  返回结果是取消的状态 True or False
# print(task1.cancel())
#
#
# #得到任务执行的结果  是阻塞的
# print(task1.result())
# print(task2.result())
# ——————————————————————————————————


urls = [2, 3, 4]

# 注意此处这种写法
all_task = [executor.submit(get_html, (url)) for url in urls]

# wait函数可以让主线程等待某些任务完成再执行下面的操作 也就是说它是阻塞的
# return_when 函数默认是等待ALL_COMPLETED 可以查看源码
wait(all_task, return_when=FIRST_COMPLETED)
print("main")
# as_completed用来获取已经完成任务的线程
for future in as_completed(all_task):
    data = future.result()
    print("get page {} success".format(data))
