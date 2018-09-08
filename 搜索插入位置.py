#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/6
def searchInsert(nums,target):  #有点慢
    if target not in nums:
        nums.append(target)
        nums.sort()
        return nums.index(target)
    else:
        return nums.index(target)

def searchInsert_two(nums,target):
    if len(nums)==0:
        return 0
    if target>nums[-1]:  #如果目标值比nums最后一个值大 直接插入
        return len(nums)
    for index in range(len(nums)):
        if nums[index]>=target:
            return index
    return len(nums)
res=searchInsert([1,3,5,6], 0)
print(res)