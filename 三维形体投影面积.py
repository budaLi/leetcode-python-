#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/9/7
def projectionArea(grid):
    """
    :type grid: List[List[int]]
    :rtype: int
    """
    res=0
    for i in range(len(grid)):
        res+=len(grid[i])+max(grid[i])-grid[i].count(0)     #注意此处不算为0的元素的长度
    tem=map(list,zip(*grid))
    for i in range(len(tem)):
        res+=max(tem[i])

    return res

res=projectionArea([[1,1,1],[1,0,1],[1,1,1]])
print(res)
