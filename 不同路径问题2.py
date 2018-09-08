#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/4

#此问题在上个问题的基础上，判断输入的数组中是否有0（障碍）有则将其设为0即可
#【【1】】 输出应为0
def unique_path(lis):#输入一个二维数组
    m=len(lis)  #行数
    if m==0:
        return 0
    n=len(lis[0])   #列数
    if m==1 or n==1:
        return 1
    for i in range(1,n):    #对于位于【0，1】和【0，n-1】之间的路只有一条路
            if lis[0][i]!=1:
                lis[0][i]=1
            else:
                lis[0][i]=0
    for j in range(1,m):    #同理
        if lis[j][0]!=1:
            lis[j][0]=1
        else:
            lis[j][0]=0
    for i in range(1,m):
        for j in range(1,n):
            if lis[i][j]==1: #如果有障碍则将其设为0
                lis[i][j]=0
            else:
                lis[i][j]=lis[i-1][j]+lis[i][j-1]
    return lis[m-1][n-1]


res=unique_path([[0,0,0],[0,1,0],[0,0,0]])
print(res)
