#-*-coding:utf8-*-
#author : Lenovo
#date: 2019/1/6

# __new__是一个静态方法 __init__是一个实例方法
# __new__会返回一个创建的类的实例 __init__什么都不会返回
# 只有当__new__返回实例后__init__才能运行
# 当创建一个实例时用__new__  当初始化实例时用__init__

# __metaclass_是创建类时起作用