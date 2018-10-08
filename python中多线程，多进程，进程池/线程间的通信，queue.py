#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/10/8
#线程间为什么需要通信
#线程间的通信方式 1，全局变量  比如 【python中的GIl】 文件中total全局变量
#queue队列

from queue import Queue

def getdetailurl(queue):
    while True:
        for i in range(20):
            queue.put('www.qnmgb.com/id={}'.format(i))
            print('put url id :{}'.format(i))

def getdetailhtml(queue):
    while True:
        url=queue.get()
        print('get url {}'.format(url))



if __name__=='__main__':
    import threading
    queue=Queue(maxsize=10)
    thread1=threading.Thread(target=getdetailurl,args=(queue,))
    thread2=threading.Thread(target=getdetailhtml,args=(queue,))
    thread1.start()
    thread2.start()
