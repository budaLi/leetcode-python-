#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/10/9
import multiprocessing
from concurrent.futures import ProcessPoolExecutor

import time
def get_html(n):    #模拟访问页面
    time.sleep(n)
    print('progress')
    return n

if __name__=='__main__':

    # progress=multiprocessing.Process(target=get_html,args=(2,))
    # print(progress.pid)
    # progress.start()
    # print(progress.pid) #只有start之后才会有Pid
    # progress.join()
    # print('end')


    # 使用线程池
    print(multiprocessing.cpu_count())  # cpu数量
    pool=multiprocessing.Pool(multiprocessing.cpu_count())  #开启几个线程
    result = pool.apply_async(get_html, args=(3,))
    pool.close()  # 在这里要注意要关闭线程池不让他再接收 不设置会报错
    pool.join()  # 等待所有任务完成
    print(result.get())

    # #imap
    # pool=multiprocessing.Pool(multiprocessing.cpu_count())  #开启几个线程
    # pool.imap(get_html,[1,5,3])
    # for result in pool.imap(get_html,[1,5,3]):
    #     print('sucess {}'.format(result))
