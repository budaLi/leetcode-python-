#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/9/30

#O(n^2)
# def productExceptSelf(nums):
#     """
#     :type nums: List[int]
#     :rtype: List[int]
#     """
#     res=[1 for i in range(len(nums))]
#     for i in range(len(nums)):
#         for j in range(len(res)):
#             if i!=j:
#                 res[j]=res[j]*nums[i]
#     return res



def productExceptSelf(nums):
    """
    :type nums: List[int]
    :rtype: List[int]
    """
    tm1=[1]
    tm2=[1]
    #tm1和tm2分别存储对应位置之前的乘积和之后的乘机
    for i in range(len(nums)-1):
        tm1.append(tm1[i]*nums[i])
        tm2.append(tm2[i]*nums[-i-1])
    print(tm1,tm2)
    for i in range(len(tm1)):   #对tm1中元素进行修改
        tm1[i]=tm1[i]*tm2[-i-1]
    return tm1

res=productExceptSelf([1,2,3,4])
print(res)