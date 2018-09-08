#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/8/18
#-1 向右 -2 向左 默认想北
#记录每一种可能的情况
#比如 向北走为 y+ 此时向左为  x- 记录为 if 北 -1 -> 西 x-
#代码表示  dir=d[(dir,commend)]
from collections import defaultdict
#作用 为字典中不存在的键提供默认值
# dic=defaultdict(bool)
# print(dic['ppp'])
def robotSim( commands, obstacles):
    dire={('北',-1):'东',('北',-2):'西',('西',-1):'北',('西',-2):'南',('东',-1):'南',('东',-2):'北',('南',-1):'西',('南',-2):'东',}
    x=y=0
    res=[]  #用来存储每一个命令对应的距离
    #对于每一个障碍 我们将其对应的坐标设为1
    d=defaultdict(int)  #默认为0
    for one in obstacles:
        d[one[0],one[1]]=1
    dirtions='北' #刚开始是北
    for one in commands:
        print(one)
        if one==-1:
            print('向右')
            dirtions=dire[(dirtions,-1)]
        if one==-2:
            print('向左')
            dirtions=dire[(dirtions,-2)]
        else:
            if dirtions=='北':
                for i in range(1,one+1):    #如果步数是5 那么一共走5步 对于每一步要判断是否遇到障碍 遇到则返回上一个点
                    y=y+1
                    if d[x,y+1]==1:
                        print('碰到障碍:',x,y+1)
                        y=y-1
                        break
            if dirtions=='南':
                for i in range(1,one+1):
                    y=y-1
                    if d[x,y-1]==1:
                        print('碰到障碍:',x,y-1)
                        y=y+1
                        break
            if dirtions=='西':
                for i in range(1,one+1):
                    x=x-1
                    if d[x-1,y]==1:
                        print('碰到障碍:',x-1,y)
                        x=x+1
                        break
            if dirtions=='东':
                for i in range(1,one+1):
                    x=x+1
                    if d[x+1,y]==1:
                        print('碰到障碍:',x+1,y)
                        x=x-1
                        break
        print('坐标:',x,y)
        res.append(pow(x,2)+pow(y,2))
        print(res)
    if res:
        return max(res)
    else:
        return 0

res=robotSim([-2,-1,4,7,8],
[[1,1],[2,1],[4,4],[5,-5],[2,-3],[-2,-3],[-1,-3],[-4,-1],[-4,3],[5,1]])
print(res)
