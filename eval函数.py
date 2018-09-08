#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/8/23
#eval函数可以将字符串转换为列表元祖字典
#str 相反


# res1='[1,2,3]'
# res2='(1,2,3,)'
# res3='{"a":3}'
# print(eval(res1))
# print(eval(res2))
# print(eval(res3))
#
# ss=[1,2,7,3,4,5]
# name=sorted(ss)
# print(name)


# def arrayPairSum(nums):
#     """
#     :type nums: List[int]
#     :rtype: int
#     """
#     res=0
#     nums=sorted(nums)
#     for i in range(0,len(nums),2):
#         res+=nums[i]
#     return res
#
# res=arrayPairSum([1,2,3,4])
# print(res)
# nums=[1,2,3,4]
# for i in range(0,len(nums),2):
#     print(nums[i])

def findContentChildren(g, s):
    if s==[]:
        return 0
    for one in sorted(g):
        if one>max(s):
            return min(len(g[:g.index(one)+1]),len(s))
    return min(len(g),len(s))


res=findContentChildren()
print(res)

