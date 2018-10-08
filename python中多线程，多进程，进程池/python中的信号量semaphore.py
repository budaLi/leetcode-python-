#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/10/8
#用于控制进入数量的锁
#场景 文件分为读和写 读可以允许右多个线程读 但是写的时候只能允许一个线程写

#在这里应该巩固一下操作系统中的生产者消费者问题

import threading
import time

from queue import Queue
#semaphore内部使用了condition条件变量实现
class Spider(threading.Thread):
    def __init__(self,url,sem):
        super(Spider, self).__init__()
        self.url=url
        self.sem=sem
    def run(self):
        time.sleep(3)
        print('start crawl')
        self.sem.release()  #在这里要注意完成爬取一次就要释放一次而不是在下面的类中释放 如果在下面释放 则变为
                            #开启一个线程释放一个 这个信号量就没有意义

class UrlProducer(threading.Thread):    #用来产生url
    def __init__(self,sem):
        super(UrlProducer, self).__init__()
        self.sem=sem
    def run(self):
        for i in range(20):
            sem.acquire()
            thread=Spider('http://wwww.baidu.com',sem)
            thread.start()

if __name__=='__main__':
    sem=threading.Semaphore(3)
    urlpro=UrlProducer(sem)
    urlpro.start()