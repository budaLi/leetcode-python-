#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/9/10
import contextlib


#上下文管理器
@contextlib.contextmanager
def file_open(file_name):
    print('file open')
    yield
    print('fielf close')

with file_open('123') as f:
    print('start')