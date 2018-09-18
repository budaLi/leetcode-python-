#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/9/5
import time
# def findErrorNums(nums):    #超出时间限制
#     """
#     :type nums: List[int]
#     :rtype: List[int]
#     """
#     start=time.time()
#     res1=0
#     res2=0
#     for i in range(1,len(nums)+1):
#         if nums.count(i)==2:
#             res1=i
#             if res2!=0: break
#         if nums.count(i)==0:
#             res2=i
#             if res1!=0: break
#     end=time.time()
#     print('time',(end-start))
#     return [res1,res2]

# def findErrorNums(nums):  #思路有问题
#     dic={}
#     los=0
#     rep=0
#     nums=list(sorted(nums))
#     print(nums)
#     for i in range(len(nums)-1,-1,-1): #倒着比
#         print(i)
#         #此处排序后 缺失值只记录一次 否则后面出现的情况会覆盖导致出错
#         if nums[i]!=i+1 and los==0: los=i+1
#         if nums[i] not in dic: dic[nums[i]]=1
#         else: rep=nums[i]
#
#     return [rep,los]


#思路 对原列表去重求和 不去重求和 以及 从1到n求和
def findErrorNums(nums):
    tem=(1+len(nums))*len(nums)/2
    print(tem)
    los=tem-sum(set(nums))
    rep=sum(nums)-sum(set(nums))

    return [rep,los]
#[3,2,3,4,6,5]
#[1,2,2,4]
#[1,5,3,2,2,7,6,4,8,9]
res=findErrorNums([3,2,3,4,6,5])
print(res)

