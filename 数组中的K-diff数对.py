#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/10/7
def findPairs(nums, k):
    """
    :type nums: List[int]
    :type k: int
    :rtype: int
    """
    count=0
    res=[]
    if k<0: return 0
    for i in range(len(nums)):
        if (nums[i]+k  in nums[:i]+nums[i+1:]):
            print(nums[i],nums[i]+k)
            if [nums[i],nums[i]+k] not in res and [nums[i]+k,nums[i]] not  in res:
                count+=1
                res.append([nums[i],nums[i]+k])
        if  (nums[i]-k  in nums[:i]+nums[i+1:]):
            print(nums[i],nums[i]-k)
            if [nums[i],nums[i]-k] not in res and [nums[i]-k,nums[i]] not in res:
                count+=1
                res.append([nums[i],nums[i]-k])
    print(res)
    return len(res)

res=findPairs([1,3,1,5,4],
1)
print(res)