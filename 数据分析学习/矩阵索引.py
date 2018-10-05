#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/10/3
import numpy as  np
print(np.arange(20))
data=np.sin(np.arange(20)).reshape(5,4)     #np.sin() 对数组中每个元素取正弦
print(data)

print(data.shape)   #(5L, 4L) 数组的维度
print(data.shape[0]) #行 5
print(data.shape[1]) #列 4

ind=data.argmax(axis=0) #返回数组种每列最大元素的索引值
print(ind)

# ind=data.argmax(axis=1) #返回数组种每行最大元素的索引值
# print(ind)


print(data[ind,range(data.shape[1])])
#根据索引得到每一列中最大的值


res=np.arange(3)    #使用np.tile对矩阵进行扩展
a=np.tile(res,(2,3))
print(a)

#排序
tem=np.array([2,3,4,1])
a=np.sort(tem)
print(a)
index=np.argsort(tem)   #从小到大排序得到索引值
print(tem[index])       #按照上面得到的索引得到排序后的元素