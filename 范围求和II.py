#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/10/5
def maxCount(m, n, ops):
    """
    :type m: int
    :type n: int
    :type ops: List[List[int]]
    :rtype: int
    """
    # nums=[[0 for i in range(m)] for j in range(n)]
    # for one in ops:
    #     for i in range(one[0]):
    #         for j in range(one[1]):
    #             nums[i][j]+=1
    # tem=0
    # for i in range(len(nums)):
    #     for j in range(len(nums[0])):
    #         tem=max(tem,nums[i][j])
    # count=0
    # for i in range(len(nums)):
    #     for j in range(len(nums[0])):
    #         if nums[i][j]==tem:
    #             count+=1
    # return count

    #实际上求操作的最小范围
    return min(i[0] for i in ops) * min(i[1] for i in ops)  if ops else m*n
res=maxCount(m = 3, n = 3,
ops = [[2,2],[3,3]])

print(res)