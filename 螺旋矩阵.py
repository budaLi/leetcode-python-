#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/13
def spiralMatrixIII(R, C, r0, c0):
    tem=[[0 for x in range(1000)] for x in range(1000)]
    flag=0
    tem[r0][c0]=1
    res=[]
    while flag<=R*C:
        tem[r0+1][c0]=tem[r0][c0]+1
        if r0+1<=R and c0<=C:
            flag=flag+1
            res.append([r0+1,c0])
        tem[r0+1][c0+1]=tem[r0+1][c0]+1
        if r0+1<=R and c0+1<=C:
            flag=flag+1
            res.append([r0+1,c0+1])
        tem[r0][c0+1]=tem[r0+1][c0+1]+1
        if r0<=R and c0+1<=C:
            flag=flag+1
            res.append([r0,c0+1])

