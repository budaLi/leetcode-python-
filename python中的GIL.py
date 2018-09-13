#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/9/13
#GIL global interpreter locck 全局解释器锁
#python中的一个线程对应于c语言中的一个线程
#gil是使得一个时刻只有一个线程在一个cpu上运行 并且无法将多个线程映射到多个cpu上

#gil会根据执行的字节码行数以及时间片释放gil 在遇到io操作的情况下主动释放

# import dis      #可以查到一个函数的字节码 也就是函数执行过程
# def add(a):
#     return a+1
#
# print(dis.dis(add))



#下面这个例子可以看出gil并不是一直锁定的 他有时候会释放  可能类似操作系统中时间片轮转法
import threading

total=0
def add():
    global total
    for i in range(10000):
        total+=1

def desc():
    global total
    for i in range(10000):
        total-=1

thread1=threading.Thread(target=add)
thread2=threading.Thread(target=desc)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print(total)