#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/10/9
#想了十分钟没有思路。。哎

#实现思路 由于二进制的特性 如 8421 如果最高为变为1那么这个数肯定比最高位不为1的数大
#根据这个思路我们应该对于矩阵的每一行进行变换 把每一行的最高位变为1 那么行就不能变了
#然后变换矩阵的列 这里每一列对应的权值都是一样的 所以我们应该使每一列的1的个数大于等于0的个数 此时这个矩阵是最大的

class Solution(object):
    def matrixScore(self, A):
        """
        :type A: List[List[int]]
        :rtype: int
        """
        m=len(A)
        if m==1:
            if A[0][0]==0:
                for i in range(len(A[0])):
                    A[0][i]=1 if A[0][i]==0 else 0
            print(A)
            return (int(''.join(map(str,A[0])),2))
        n=len(A[0])
        for i in range(m):  #对每一行使第一个数都为1
            if A[i][0]==0:
                for j in range(n):
                    A[i][j]=1 if A[i][j]==0 else 0
        for i in range(1,n):    #从第二列开始 使每一列1尽可能多
            count=0
            for j in range(m):
                if A[j][i]==0:
                    count+=1
            if count>m/2:
                for j in range(m):
                    A[j][i]=1 if A[j][i]==0 else 0
        res=0
        print(A)
        for i in range(m):
            res+=(int(''.join(map(str,A[i])),2))
        return res

S=Solution()
res=S.matrixScore([[0,1],[0,1],[0,1],[0,0]])
print(res)
