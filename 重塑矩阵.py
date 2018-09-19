#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/9/19
def matrixReshape(nums, r, c):
    """
    :type nums: List[List[int]]
    :type r: int
    :type c: int
    :rtype: List[List[int]]
    """
    w=len(nums)
    h=len(nums[0])
    if w*h!=r*c: return nums
    #将原数组中的值存放在一个一维数组 再放到新的列表中
    res=[]
    for one in nums:
        res.extend(one)
    tems=[[0 for i in range(c)] for j in range(r)]
    for i in range(r):
        for j in range(c):
            tems[i][j]=res.pop(0)

    return tems

res=matrixReshape(nums =
[[1,2],
 [3,4]],
r = 1, c = 3)
print(res)
