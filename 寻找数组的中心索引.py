#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/27
def pivotIndex(nums):
    """
    :type nums: List[int]
    :rtype: int
    """

    if len(nums)==1:
        return len(nums)
    tem=0
    tem2=sum(nums)-nums[0]
    if tem==tem2:
        return 0
    for i in range(1,len(nums)):
        if tem+nums[i-1]==tem2-nums[i]:
            return i
        tem=tem+nums[i-1]
        tem2=tem2-nums[i]
    return -1

res=pivotIndex([1,7,3,6,5,6])
print(res)