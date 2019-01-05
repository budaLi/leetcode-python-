#-*-coding:utf8-*-
#author : Lenovo
#date: 2019/1/5


dic={value:key for key,value in enumerate([1,2,3])}
print(dic)

#比如用上述方式可以将一个可迭代对象中的数据 变为 键为值 值为索引的形式
#这样就可以通过其值得到其索引了