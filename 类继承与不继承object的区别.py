#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/1
class A(object):    #继承object为新式类   采用广度优先搜索
    def foo(self):
        print('A.foo')
class B(A):
    pass
class C(A):
    def foo(self):
        print('C.foo')

class D(B,C):
    pass


d=D()
print(d.foo())
#result:C.foo()


class M:    #没有继承object为经典类 采用深度优先搜索
    def foo(self):
        print('M.foo')
class N(M):
    pass

class O(A):
    def foo(self):
        print('O.foo')
class Q(N,O):
    pass

q=Q()
print(q.foo())