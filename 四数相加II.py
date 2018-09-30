#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/9/30

#O（n^4)
# def fourSumCount(A, B, C, D):
#     """
#     :type A: List[int]
#     :type B: List[int]
#     :type C: List[int]
#     :type D: List[int]
#     :rtype: int
#     """
#     count=0
#     for i in A:
#         for j in B:
#             for k in C:
#                 for o in D:
#                     if i+j+k+o==0:
#                         count+=1
#     return count

#先存储其中两个的值
def fourSumCount(A, B, C, D):
    """
    :type A: List[int]
    :type B: List[int]
    :type C: List[int]
    :type D: List[int]
    :rtype: int
    """
    from collections import Counter
    tem=[]
    count=0
    for i in C:
        for j in D:
            tem.append(i+j)
    print(tem)
    com=Counter(tem) #快速返回列表中元素个数，但结果是按照元素出现的次数降序排列
    for i in A:
        for j in B:
            print(i,j)
            if -(i+j) in com:   #此处不用tem
                count+=com[-(i+j)]    #此处需要注意如果CD中有重复出现值 count也要+ 但是count很耗时

    return count

res=fourSumCount([-1,-1],
[-1,1],
[-1,1],
[1,-1],
)
print(res)