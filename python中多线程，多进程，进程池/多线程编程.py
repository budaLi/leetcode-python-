#-*-coding:utf8 -*-
#author : Lenovo
#date: 2018/10/8
#操作系统能够调度和分配的最小单元是线程
#在最开始的时候操作系统能够调度的基本单位是进程 由于进程对系统消耗资源过大 从而产生线程
#对于以IO操作为主的任务来说 多进程和多线程性能差别不大

import time
#1 通过Thread实例化
def get_detail_html(url):
    print('get detail html start')
    time.sleep(2)
    print('get detail html end')

def get_detail_url(url):
    print('get detail url start ')
    time.sleep(2)
    print('get detail url end')

import threading


if __name__=='__main__':
    thread1=threading.Thread(target=get_detail_url,args=('',))  #在这里要注意参数的书写格式 应该在元组里
    thread2=threading.Thread(target=get_detail_html,args=("",))
    #thread1.setDaemon(True) #当设置setDaemon时 主线程关闭时两个子线程也会关闭 此时两个线程被设置为主线程的守护线程
                            #如果在这里不设置两个线程的setDeamon为True,那么结果为：
                            #get detail url start
                            # get detail html start
                            # get detail url end
                            # get detail html end

                            #原因是 当线程1开启后输出语句为执行IO操作，线程会切换 此时线程2执行输出语句
                            #此时再次切换到线程1 等待两秒后线程1 输出结束语句 切换到线程2 立即输出结束语句
    thread1.join()      #当设置线程 join时 主线程会等到两个线程运行完后 再运行主线程
    thread2.join()


    #thread2.setDaemon(True)
    thread1.start()
    thread2.start()

#实现多线程的方法2  通过继承thread的Thread类来实现

class GetDetailHaml(threading.Thread):
    def run(self):
        pass

class GetDetailUrl(threading.Thread):
    def run(self):
        pass

