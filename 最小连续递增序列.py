#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/9/1
def findLengthOfLCIS(nums):
    """
    :type nums: List[int]
    :rtype: int
    """
    length=len(nums)
    if len(set(nums))<=1:
        return len(set(nums))
    i=0
    res=0
    count=1
    for j in range(1,length):
        if nums[i]<nums[j]:
            count+=1
            i+=1
        else:
            i=j
            count=1
        res=max(res,count)
    return res
res=findLengthOfLCIS([1,3,5,4,7,4,5,6,7])
print(res)