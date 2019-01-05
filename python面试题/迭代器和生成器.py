#-*-coding:utf8-*-
#author : Lenovo
#date: 2019/1/5
# 将列表生成式中[]改成() 之后数据结构是否改变？ 答案：是，从列表变为生成器

#迭代器
L = [x*x for x in range(1222)]


#将[ 改为 （  就变为生成器了

g = (x for x in range(1000000000000))


# print(type(L))
# print(type(g))
#
# print(L)    #这样会直接得到迭代器中的所有元素
# print(g)    #而生成器对象只能通过for循环的方式访问
# for one in g:
#     print(one)

#通过列表生成式 可以生成一个拥有多个数据的列表 一次性生成 但是这样由于收到内存限制 生成数据的数量肯定是有限的

#而且创建一个百万级的列表 不仅消耗内存 当我们仅需要前面的几个数据时  后面的很大空间都浪费了

#这时我们可以采用迭代器 边循环边计算的方式

import itertools

for x in itertools.product([1,2,3]):
    print(x)

import os

print(os.path.isfile("01矩阵.py"))

