#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/9/18


#规律 res=int(sqrt(n))
def bulbSwitch(n):
    """
    :type n: int
    :rtype: int
    """
    res=[1 for i in range(n)]   #1代表开着
    for i in range(2,n+1):    #轮数
        for j in range(i-1,n,i):
            res[j]=res[j]^1 if res[j]==0 else 0
        print(res)
    return res.count(1)


res=bulbSwitch(4)
print(res)
