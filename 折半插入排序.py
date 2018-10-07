#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/10/7

#还有问题 网上找的代码也有问题 很难受
#折半插入排序 在冒泡排序的基础上搜索插入位置时使用二分查找
def binaryinsertsort(alist):
    for index in range(1, len(alist)):
        currentvalue = alist[index]
        position = index

        while position > 0 and alist[position-1] > currentvalue:
            alist[position] = alist[position-1]
            position -= 1
        alist[position] = currentvalue

    return alist

res=binaryinsertsort([4,2,1,3,5])
print(res)

