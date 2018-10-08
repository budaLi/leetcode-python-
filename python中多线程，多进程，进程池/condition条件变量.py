#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/9/16
from threading import Condition
#条件变量 用于复杂的下线程同步
import threading
import time

class Xiaoai(threading.Thread):
    def __init__(self,cond):
        super(Xiaoai, self).__init__(name='小艾')
        self.cond=cond

    def run(self):
        with self.cond:
            self.cond.wait()
            time.sleep(2)
            print('{}：在'.format(self.name))
            self.cond.notify()

            self.cond.wait()
            time.sleep(2)
            print('{}：你好'.format(self.name))
            self.cond.notify()

class Tianmao(threading.Thread):
    def __init__(self,cond):
        super(Tianmao, self).__init__(name='挑毛')
        self.cond=cond

    def run(self):
        with self.cond:
            print('{}：小艾同学'.format(self.name))
            self.cond.notify()
            self.cond.wait()

            time.sleep(2)

            print('{}：么么哒'.format(self.name))
            self.cond.notify()
            self.cond.wait()


if __name__=='__main__':
    cond=Condition()
    xiaoai=Xiaoai(cond)
    tianmao=Tianmao(cond)

    #注意此处顺序
    xiaoai.start()
    tianmao.start()

