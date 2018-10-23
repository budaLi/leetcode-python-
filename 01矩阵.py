#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/10/18
class Solution(object):     #有待思考 BFS  广度优先算法
    def updateMatrix(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: List[List[int]]
        """
        for one in matrix:
            print(one)
        w=len(matrix)
        if w==1:    #变为一维矩阵
            for i in range(matrix[0]):
                pass
        w=len(matrix)-1
        h=len(matrix[0])-1
        for i in range(w+1):
            for j in range(h+1):
                if matrix[i][j]!=0:
                    if (0<=i-1<=w and 0<=j<=h and matrix[i-1][j]==0) or (0<=i+1<=w and 0<=j<=h and matrix[i+1][j]==0) or (0<=i<=w and 0<=j-1<=h and matrix[i][j-1]==0) or (0<=i<=w and 0<=j+1<=h and matrix[i][j+1]==0):
                        matrix[i][j]=1
                    else:       #左边和上边距离的最小值加1
                        tem=[]
                        if (0<=i-1<=w and 0<=j<=h):
                            tem.append(matrix[i-1][j])
                        if (0<=i<=w and 0<=j-1<=h):
                            tem.append(matrix[i][j-1])
                        matrix[i][j]=min(tem)+1
        return matrix

S=Solution()
res=S.updateMatrix([[1, 0, 1, 1, 0, 0, 1, 0, 0, 1], [0, 1, 1, 0, 1, 0, 1, 0, 1, 1], [0, 0, 1, 0, 1, 0, 0, 1, 0, 0], [1, 0, 1, 0, 1, 1, 1, 1, 1, 1], [0, 1, 0, 1, 1, 0, 0, 0, 0, 1], [0, 0, 1, 0, 1, 1, 1, 0, 1, 0], [0, 1, 0, 1, 0, 1, 0, 0, 1, 1], [1, 0, 0, 0, 1, 1, 1, 1, 0, 1], [1, 1, 1, 1, 1, 1, 1, 0, 1, 0], [1, 1, 1, 1, 0, 1, 0, 0, 1, 1]])
for one in res:
    print(one)