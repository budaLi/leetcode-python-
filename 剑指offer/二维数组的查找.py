#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/10/23
class Solution:
    # array 二维列表
    def Find(self, target, array):
        # write code here
        def binaryfind(s,target):
            low=0
            high=len(s)-1
            while low<high:
                mid=(low+high)//2
                if s[mid]==target:
                    return mid
                elif s[mid]>target:
                    high=mid-1
                else:
                    low=mid+1
            return low
        if len(array)==0 or len(array[0])==0: return False #考虑列表为空的情况
        if len(array)==1:
            index=binaryfind(array[0],target)
            return array[0][index]==target
        tem=[array[i][0] for i in range(len(array))]
        index=binaryfind(tem,target)    #找出所有可能存在目标值的行
        print(index)
        for i in range(0,index+1):    #对每一行进行查找
            res=binaryfind(array[i],target)
            if array[i][res]==target:
                return True
        return False
S=Solution()
res=S.Find(16,[[1,16]])
print(res)