#-* -coding:utf8 -*-
#author : Lenovo
#date: 2018/9/18

#思路是初始化时存储前x个元素之和
#例如 res[1] 代表存储前1个元素之和
class NumArray(object):

    def __init__(self, nums):
        """
        :type nums: List[int]
        """
        if len(nums)==0:
            self.res=[]
        else:
            self.res=[0 for i in range(len(nums))]
            self.res[0]=nums[0]
            for i in range(1,len(nums)):
                self.res[i]=self.res[i-1]+nums[i]

    def sumRange(self, i, j):
        """
        :type i: int
        :type j: int
        :rtype: int
        """
        if self.res==[]: return 0
        #存储的是前x个元素之和 所以区间值等于 前j个元素之和减去前i-1个元素之和
        if i==0: return self.res[j]
        return self.res[j]-self.res[i-1]


obj = NumArray([-2, 0, 3, -5, 2, -1])
param_1 = obj.sumRange(2,5)
print(param_1)