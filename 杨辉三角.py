#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/10/5
def generate(numRows):
    """
    :type numRows: int
    :rtype: List[List[int]]
    """
    res=[1]
    ans=[[1]]
    for i in range(1,numRows):
        res=[1]+[res[i]+res[i+1] for i in range(len(res)-1)]+[1]
        ans.append(res)
    return ans

res=generate(5)
print(res)