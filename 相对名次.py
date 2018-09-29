#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/9/21
def findRelativeRanks(nums):
    """
    :type nums: List[int]
    :rtype: List[str]
    """
    # gold=["Gold Medal", "Silver Medal", "Bronze Medal"]
    # tem=sorted(nums,reverse=True)
    # print(tem)
    # for i in range(len(tem[:3])):
    #     print(gold[i])
    #     tem[i]=gold[i]
    # for i in range(3,len(tem)):
    #     print(tem[i])
    #     tem[i]=str(i+1)
    # return tem

    sort = sorted(nums)[::-1]
    rank = ["Gold Medal", "Silver Medal", "Bronze Medal"] + map(str, range(4, len(nums) + 1))
    return map(dict(zip(sort, rank)).get, nums)

import random
ss={random.randrange(1,100) for i in range(100)}
res=findRelativeRanks(ss)
print(res)