#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/9/10
# def singleNumber(nums):
#     """
#     :type nums: List[int]
#     :rtype: int
#    """
#     for i in range(len(nums)):    #什么都不是的垃圾
#         print(nums)
#         if len(nums)==1: return nums[0]
#         nums=sorted(nums)
#         mid=len(nums)/2
#         print(nums)
#         if nums[mid]!=nums[mid-1] and nums[mid]!=nums[mid+1]:
#             return nums[mid]
#         elif nums[mid]==nums[mid-1]:
#             nums=nums[:mid-1]
#         else:
#             nums=nums[mid+1:]
def singleNumber(nums):     #0异或任何数不变，任何数与自己异或为0。a⊕b⊕a=b
        res = 0
        for i in nums:
            res^=i
        return res

res=singleNumber([4,1,2,1,2])
print(res)


print(~30)      #~a=-a-1