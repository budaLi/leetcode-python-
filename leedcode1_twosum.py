#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/7/23
class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        d = {}# d is a dictionary to map the value of nums and the index in nums
        size = 0
        for size in range(len(nums)):
            if not nums[size] in d:
                d[nums[size]] = size  #if nums[size] doesn't exist in d ,create it
            if target - nums[size] in d: #if nums[size] and target - nums[size] are both in d
                # if d[target-nums[size]] < size + 1: # one situation should be minded nums[size] == target - nums[size]
                    ans = [d[target - nums[size]] , size ]# for example [0,1,2] 0 and [0,1,2,0],0
                    return ans
ex=Solution()
e=ex.twoSum([1,2,5,7,8],16)
print(e)