#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/8/14
A=[1,2,3,4]
B=['a','b','c','d']
C={'A':1,'B':2}

A.append(B)         #append是将添加的元素直接加在后面,添加后列表多一个元素
print(A)            #可以添加列表 元祖 字典

A.append(C)
print(A)

A.extend(B)     #extend是将可迭代的对象依次加入 被添加者必须可迭代
print(A)

A.extend(C)     #extend如果添加的是字典 默认添加字典的键 当使用C.vlues() 时添加值
print(A)

A.pop()     #pop是将列表中的元素按照索引值弹出 默认为最后一个 也就是-1 他会返回被弹出的元素的值
a=C.pop('A')      #d当字典对象使用pop时，需要指定key
print(C)
print(a)        #当字典接受pop时 只会接受被弹出的值

A.remove(1) #remmove是将列表中的值按值弹出，必须有参数
            #字典对象没有remove函数

del A[1:3]      #del 关键字按指定切片删除列表中的元素 并返回新的列表
print(A)

del A       #当直接删除一个列表时 再次打印该列表报错
print(A)
