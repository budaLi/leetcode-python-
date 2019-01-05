#-*-coding:utf8-*-
#author : Lenovo
#date: 2019/1/5


class Test():
    def __init__(self):
        self._node=1
        self.__node=2


A=Test()
print(A._node)


#__xxx__ 这种形式代表这个是Python内部类型  以区分和用户使用

#_xxx  是一种约定的方式  表示不能用from ** import 这种方式引入


#__xxx 是真正意义上的私有变量 系统将其变为_classname__xxx这种名称  也可以访问