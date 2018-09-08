#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/8/3


def  solution(m,n): #输入m行n列
    if m<=0 or m>100 or n<=0 or n>100:
        return 0
    if m==1 or n==1:
        return 1
    d = [[0 for i in range(n)] for i in range(m)]   #初始化
    for i in range(1,n):    #对于位于【0，1】和【0，n-1】之间的路只有一条路
        d[0][i]=1
    for j in range(1,m):    #同理
        d[j][0]=1
    for i in range(1,m):
        for j in range(1,n):
            if d[i][j]!=1:
                d[i][j]=d[i-1][j]+d[i][j-1]
    return d[m-1][n-1]


res=solution(3,3)
print(res)
