#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/9/4
def imageSmoother(M):
    """
    :type M: List[List[int]]
    :rtype: List[List[int]]
    """
    import copy
    Mtem=copy.deepcopy(M)
    x=len(M)
    y=len(M[0])
    if x== 1 and y==1:return M
    if x==1:
        for i in range(y):
            if i==0: Mtem[0][i]=int((M[0][i]+M[0][i+1])/2)
            elif i==y-1:
                Mtem[0][i]=int((M[0][i-1]+M[0][i])/2)
                return Mtem
            else:
                Mtem[0][i]=int((M[0][i]+M[0][i-1]+M[0][i+1])/3)

    if y==1:
        for i in range(x):
            if i==0: Mtem[i][0]=int((M[i][0]+M[i+1][0])/2)
            elif i==x-1:
                Mtem[i][0]=int((M[i-1][0]+M[i][0])/2)
                return Mtem
            else:
                Mtem[i][0]=int((M[i][0]+M[i-1][0]+M[i+1][0])/3)

    Mtem[0][0]=int((M[0][0]+M[0][1]+M[1][0]+M[1][1])/4)        #四个顶顶
    Mtem[0][y-1]=int((M[0][y-1]+M[0][y-2]+M[1][y-2]+M[1][y-1])/4)
    Mtem[x-1][0]=int((M[x-1][0]+M[x-2][0]+M[x-2][1]+M[x-1][1])/4)
    Mtem[x-1][y-1]=int((M[x-1][y-1]+M[x-2][y-1]+M[x-2][y-2]+M[x-1][y-2])/4)
    if x ==2 and y==2:
        return Mtem
    for i in range(1,x-1):
        Mtem[i][0]=int((M[i][0]+M[i-1][0]+M[i-1][1]+M[i][1]+M[i+1][1]+M[i+1][0])/6)
        Mtem[i][y-1]=int((M[i][y-1]+M[i-1][y-1]+M[i-1][y-2]+M[i][y-2]+M[i+1][y-2]+M[i+1][y-1])/6)
    for j in range(1,y-1):
        Mtem[0][j]=int((M[0][j]+M[0][j-1]+M[1][j-1]+M[0][j+1]+M[1][j]+M[1][j+1])/6)
        Mtem[x-1][j]=int((M[x-1][j]+M[x-1][j-1]+M[x-2][j-1]+M[x-2][j]+M[x-2][j+1]+M[x-1][j+1])/6)
    for i in range(1,x-1):
        for j in range(1,y-1):
            Mtem[i][j]=int((M[i][j]+M[i-1][j]+M[i-1][j-1]+M[i][j-1]+M[i+1][j-1]+M[i+1][j]+M[i+1][j+1]+M[i][j+1]+M[i-1][j+1])/9)

    return Mtem

res=imageSmoother([[2,5,8],[4,0,1]])
print(res)