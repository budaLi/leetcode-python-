#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/8/27
#当生成一个类的对象时 new函数先调用 init函数再调用
#new 函数用来生成一个类的实例 init只是为这个实例 添加属性等 它发生在这个实例被创建之后
# class A(object):
#     def __init__(self,name):
#         print(123)
#         self.name=name
#     def __new__(cls,name):
#         print(234)
#         return super(A, cls).__new__(cls,name)
# a=A(123)


#当我们想继承一些不可变的类时 可用new来改变他们的初始化过程 但init只能做赋值

class A(int):
    def __init__(self,val):
        super(A, self).__init__(self,abs(val))
a=A(-10)
print(a)

#如下可以用new
#def __new__(cls,name):
#return super(B,cls).__new__(cls,val)
class B(int):
    def __new__(cls,val):
        return super(B, cls).__new__(cls,abs(val))

b=B(-10)
print(b)