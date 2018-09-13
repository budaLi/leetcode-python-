#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/9/13
import time
import threading

def test1():
    print('1 start')
    time.sleep(2)
    print('1 end')

def test2():
    print('2 start')
    time.sleep(4)
    print('2 end')

thread1=threading.Thread(target=test1)
thread2=threading.Thread(target=test2)

thread1.setDaemon(True)    #将线程定义为守护线程 在主线程结束时不管 其运行完了没 都将其结束

thread1.start()
thread2.start()
start_time=time.time()

thread1.join()
thread2.join()      #使得线程阻塞 当这个线程运行完之后才会运行主线程 这两个线程是并发执行的 也就是说执行的时间为两者最大时间
print('time is {}'.format(start_time-time.time()))
#此处共有三个线程 主线程 和两个其他线程