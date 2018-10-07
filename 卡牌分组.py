#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/10/7
def hasGroupsSizeX(deck):
    """
    :type deck: List[int]
    :rtype: bool
    """
    dic={}
    if len(deck)==1: return False
    if len(set(deck))==1: return True
    for one in deck:
        if one not in dic:
            dic[one]=1
        else:
            dic[one]+=1
    tem=1
    for j in range(2,max(dic.values())+1):
        #all函数 参数中所有满足条件则返回true
        if all(dic.values()[k]%j==0 for k in range(len(dic.values()))):
            tem=j
    return tem!=1

#[1,1,1,1,2,2,2,2,2,2] 第一次未通过 特例
#[1,1,1,2,2,2,3,3]
#说明如果具有大于1的公因子则也可以
res=hasGroupsSizeX([1,1,1,1,2,2,2,2,2,2])
print(res)