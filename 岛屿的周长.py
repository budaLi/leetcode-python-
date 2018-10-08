#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/10/8
def islandPerimeter(grid):
    """
    :type grid: List[List[int]]
    :rtype: int
    """
    dic={}
    w=len(grid)
    count=0
    if w==1:
        for i  in range(len(grid[0])-1):
            if grid[0][i]==1:
                count+=4
                if grid[0][i+1]==1:
                    count-=2
        if grid[0][-1]==1: count+=4
        return count
    h=len(grid[0])
    for i in range(w):
        for j in range(h):
            if grid[i][j]==1:
                dic[(i,j)]=1
    print(dic)
    for one in dic:
        if (one[0]+1,one[1]) in dic:
            count-=2
        if (one[0],one[1]+1) in dic:
            count-=2
    print(count)
    print(len(dic))
    count+=len(dic)*4

    return count

res=islandPerimeter([[0,1,0,0],
 [1,1,1,0],
 [0,1,0,0],
 [1,1,0,0]])
print(res)