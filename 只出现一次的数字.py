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
def singleNumber(nums):     #0异或任何数不变。
        res = 0
        for i in nums:
            tem=res
            res^=i
            print(tem,i,res)
        return res

res=singleNumber([4,1,2,1,2])
print(res)

