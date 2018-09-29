#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/9/29
#案例 某网络游戏中 定义了玩家类 每有一个在线玩家 服务器将会有一个实例对象
#当在线人数很多事 将产生大量实例 如何降低这些实例的内存开销

#定义类的__slots__属性 他是用来声明实例属性名字的列表


class Play1(object):
    def __init__(self,id,name):
        self.id=id
        self.name=name

p1=Play1(1,'libuda')
print(p1.__dict__)
# p1.x=1
# print(p1.__dict__)
#上面例子中由于存在__dict__ 是允许动态添加属性的
#由于dict是消耗内存的那么当量较大时消耗内存
import sys
print(sys.getsizeof(p1.__dict__))
#我们可以使用sys的方法查看使用内存情况

class Play2(object):
    __slots__=['id','name']
    def __init__(self,id,name):
        self.id=id
        self.name=name

#当我们用__stlots__定义后 不允许动态添加属性 添加时会报错

p2=Play2(2,'buda')

# p2.x=1 #报错

print(sys.getsizeof(p2))
#此时已经不能用dict了