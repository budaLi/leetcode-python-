#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/10/7
# def findPairs(nums, k):     #不是最佳方法 超出时间限制
#     """
#     :type nums: List[int]
#     :type k: int
#     :rtype: int
#     """
#     count=0
#     res=[]
#     if k<0: return 0
#     for i in range(len(nums)):
#         if (nums[i]+k  in nums[:i]+nums[i+1:]):
#             print(nums[i],nums[i]+k)
#             if [nums[i],nums[i]+k] not in res and [nums[i]+k,nums[i]] not  in res:
#                 count+=1
#                 res.append([nums[i],nums[i]+k])
#         if  (nums[i]-k  in nums[:i]+nums[i+1:]):
#             print(nums[i],nums[i]-k)
#             if [nums[i],nums[i]-k] not in res and [nums[i]-k,nums[i]] not in res:
#                 count+=1
#                 res.append([nums[i],nums[i]-k])
#     print(res)
#     return len(res)


def findPairs(nums, k):     #用字典先将对应的值存起来 重复的数值加1
    """
    :type nums: List[int]
    :type k: int
    :rtype: int
    """
    if k<0: return 0 #如果k小于0 则没有符合的
    dic={}
    for one in nums:
        if one not  in dic:
            dic[one]=1
        else:
            dic[one]+=1
    count=0
    if k==0:
        for one in dic:
            if dic[one]>=2: count+=1
        return count
    print(dic)
    for one in dic:
        if one+k in dic:
            print(one,dic[one]+k)
            count+=1
    return count
res=findPairs([1,2,3,5,4],
1)
print(res)