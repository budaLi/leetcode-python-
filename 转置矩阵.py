#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/9/7
def transpose(A):
    """
    :type A: List[List[int]]
    :rtype: List[List[int]]
    """
    return map(list,zip(*A))
    #*可以将A变为里面的元素
res=transpose([[1,2,3],[4,5,6],[7,8,9]])
print(res)
