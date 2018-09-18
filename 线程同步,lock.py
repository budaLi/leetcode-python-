#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/9/16
#使用锁实现线程同步

total=0
from threading import Lock
import threading
lock=Lock()


#注意不恰当的锁会引起思索 资源竞争
def add():
    global lock,total
    lock.acquire()
    total+=1
    lock.release()

def desc():
    global lock,total
    lock.acquire()
    total-=1
    lock.release()

thread1=threading.Thread(target=(add))
thread2=threading.Thread(target=(desc))

thread1.start()
thread2.start()

print(total)