#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/8/26
class Company(object):
    def __init__(self,sal):
        self.sal=sal
    def __getitem__(self, item):    #当对类的对象循环时 尝试从0开始访问这个类的属性 知道抛出异常
        return self.sal[item]

com=Company(['1',2,3,'4'])
for one in com:
    print(one)

#and or
# print( 0 and 2)
print(2 or 1 and 0)