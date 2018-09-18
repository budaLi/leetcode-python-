#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/9/17
# 给定一个包含 n 个整数的数组 nums，判断 nums 中是否存在三个元素 a，b，c ，使得 a + b + c = 0 ？找出所有满足条件且不重复的三元组。
# 注意：答案中不可以包含重复的三元组。
# 例如, 给定数组 nums = [-1, 0, 1, 2, -1, -4]，
# 满足要求的三元组集合为：
# [
#   [-1, 0, 1],
#   [-1, -1, 2]
# ]


#暴力遍历 n**3 不出意外超出时间限制
# def threeSum(nums):
#     """
#     :type nums: List[int]
#     :rtype: List[List[int]]
#     """
#     if len(nums)<3: return []
#     res=[]
#     for i,a in enumerate(nums):
#         for j,b in enumerate(nums):
#             for k,c in enumerate(nums):
#                 if a+b+c==0 and i!=j and j!=k and i!=k:
#                     if [a,b,c] not in res and [a,c,b] not in res and [b,a,c] not in res and [b,c,a] not in res and [c,a,b] not in res and [c,b,a] not in res:
#                         res.append([a,b,c])
#
#     return res



def threeSum(nums):
    ans = []
    nums.sort()
    for i in range(len(nums)-2):
        if i == 0 or nums[i] > nums[i-1]:
            left = i+1
            right = len(nums)-1
            while left < right:
                ident = nums[left] + nums[right] + nums[i]
                if ident == 0:
                    ans.append([nums[i], nums[left], nums[right]])
                    left += 1; right -= 1
                    while left < right and nums[left] == nums[left-1]:    # skip duplicates
                        left += 1
                    while left < right and nums[right] == nums[right+1]:
                        right -= 1
                elif ident < 0:
                    left += 1
                else:
                    right -= 1
    return ans