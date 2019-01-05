#-*-coding:utf8-*-
#author : Lenovo
#date: 2019/1/5


#自省就是 在程序运行时能知道对象的类型
#如type  得到对象的类型 如str int list dic等
#isinstance 判断变量和某个类型是否是同一类型 返回bool值
#dir  得到这个变量所有的属性
#
a=[123]
print(type(a))
print(isinstance(a,list))
print(dir(a))
print(getattr(a,"__add__"))