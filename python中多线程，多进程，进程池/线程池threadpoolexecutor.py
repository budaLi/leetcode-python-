#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/10/8

#这个包是用来线程池和进程池编程的
from concurrent import futures

#线程池 为什么需要线程池
#我们在进行爬虫的时候 希望并发进行爬取
#我们希望在主线程中可以获取某一个线程的状态 以及其返回值 或者当一个线程完成时我们能够立即知道
#futures可以让多线程和多进程接口编码一致  所谓一致指的是 当我们可以用多线程的接口时 我们可以很方便的知道多进程的编写


from concurrent.futures import ThreadPoolExecutor

import time
def gethtml(times):
    time.sleep(times)
    print('get page :{}'.format(times))

executer=ThreadPoolExecutor(max_workers=2)  #参数为线程池的可同时执行的数量

#通过submit函数提交要执行的函数以及参数

task1=executer.submit(gethtml,(3))
task2=executer.submit(gethtml,(2))

#我们注意到submit是有返回值的 我们可以根据这个返回值 知道这个任务是否完成成功
print(task1.done()) #判断任务是否返回成功
time.sleep(3)
print(task2.done())
print(task2.result())   #可以得到任务的执行结果

