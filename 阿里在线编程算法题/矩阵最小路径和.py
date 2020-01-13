# @Time    : 2020/1/13 18:29
# @Author  : Libuda
# @FileName: 矩阵最小路径和.py
# @Software: PyCharm
def Solution(m):
    """
    m为n*n的矩阵
    :param m:
    :return:
    """

    endx = len(m)-1
    if endx==0:
        #只有一行
        return sum(m[0])
    endy = len(m[0])-1
    if endy==0:
        #只有一列
        return sum(s[0] for s in m)

    #更新每一行第一个元素
    for i in range(1,endx+1):
        m[i][0]+=m[i-1][0]

    for one in m:
        print(one)
    #更新第一行的元素
    for j in range(1,endy+1):
        m[0][j]+=m[0][j-1]

    for one in m:
        print(one)

    for i in range(1,endx+1):
        for j in range(1,endy+1):
            m[i][j]+=min(m[i-1][j],m[i][j-1])

    return m[endx][endy]
"""
动态规划 只需要循环一次  到右下角的最小值=min(左边,上边)+自己的值
4 1 1 1         4  5  6  7
0 2 7 1   -->   4  6  13 8
0 5 2 1   -->   4  9  11 9
8 4 0 5         12 13 11 14


[4, 1, 5, 3]
[7, 2, 7, 7]
[13, 5, 2, 8]
[21, 9, 4, 5]
"""
# m=[[4,1,1,1], [0,2, 7,1 ],[0,5, 2,1],[8,4,0,5]]
m=[[4,1,5,3], [3,2, 7,7 ],[6,5, 2,8],[8,9,4,5]]
print(Solution(m))