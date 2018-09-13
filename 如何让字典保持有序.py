#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/9/13


import random
import string
from collections import OrderedDict

d=OrderedDict() #生成有序的字典
for i in range(52):
    for one in string.ascii_letters:    #生成a-z A-Z个人
        d[one]=random.randint(1,100)    #每个人对应一个随机成绩
print(d)

#使用字典可以提高查询的效率
#使用 OrderDict 可以使字典有序
print(d['a'])