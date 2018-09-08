#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/28
def findShortestSubArray(nums):
    """
    :type nums: List[int]
    :rtype: int
    """
    #先求出数组的度
    res=[]
    for one in range(nums):
        if one not in res:
            res[one]=nums.count(one)
    du=(max(res[i][1]) for i in range(len(res)))
res={}
nums=[1,1,2,3,4,5]
for one in nums:
    print(one)
    if one not in res:
        res[str(one)]=nums.count(one)
print(res)
du=sorted(res.items(),key=lambda x:x[1])
print(du)
