#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/10/9
#由于Python中GIL锁的限制 python无法利用多核cpu的特点
#对于IO操作来说 瓶颈不在于多线程和多进程 多线程比多进程好 因为进程间的切换是需要花费时间的
import time
from concurrent.futures import ThreadPoolExecutor,as_completed
from concurrent.futures import ProcessPoolExecutor

# #1.耗费cpu的操作 比如图像处理 以及机器学习的算法 比特币挖矿 此时多进程优于多线程
# #斐波那契数列
# def fib(n):
#     if n<=2: return 1
#     return fib(n-1)+fib(n-2)
#
# if __name__=='__main__':
#     #在这里更改ProcessPoolExecutor或者ThreadPoolExecutor就可以切换多进程和多线程 要注意的是多进程需要使用if __name__=='__main__':
#     #对斐波那契数列数列的25-40项进行测试 多线程 102秒 多进程 20秒 实在是可怕。。。
#     with ProcessPoolExecutor(3) as excutor: #在这里可以设置开启几个线程或几个进程
#         all_task=[excutor.submit(fib,(num)) for num in range(25,40)]
#         start_time=time.time()
#         for future in as_completed(all_task):
#             data=future.result()    #可以返回程序执行完成的结果
#             print('result:{}'.format(data))
#         print('time is {}'.format(time.time()-start_time))

#-----------------------------------------------------------------------------------------------------------
#对于IO操作来说 多线程优于多进程
def random(n):
    time.sleep(n)   #用sleep模拟输入输出
    return n

if __name__=='__main__':
    #在这里更改ProcessPoolExecutor或者ThreadPoolExecutor就可以切换多进程和多线程 要注意的是多进程需要使用if __name__=='__main__':
    #对斐波那契数列数列的25-40项进行测试 多线程 102秒 多进程 20秒 实在是可怕。。。
    with ProcessPoolExecutor(3) as excutor: #在这里可以设置开启几个线程或几个进程
        all_task = [excutor.submit(random, (num)) for num in range(1, 5)]
        start_time=time.time()
        for future in as_completed(all_task):
            data=future.result()    #可以返回程序执行完成的结果
            print('result:{}'.format(data))
        print('time is {}'.format(time.time()-start_time))

