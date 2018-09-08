#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/9/4

def minCostClimbingStairs(cost):
    """
    :type cost: List[int]
    :rtype: int

    """
    f1=f2=0
    for x in reversed(cost):
        f1,f2=x+min(f1,f2),f1   #用f1，f2轮流遍历列表，轮流保存最小值
    return min(f1,f2)
#思路从列表第一个元素开始，比较出当前值加上一个元素和当前值加上第二个元素的较小值
#更新并存储
#   设f1为0   当前值
#   f2=min(f1+cost[0],f1+cost[1])
#   f1=f2 存储更新后的值 即为当前值
#  相当于 f1,f2=f2,min(f1+cost[0],f1+cost[1])
ss=minCostClimbingStairs([10, 15, 20])
print(ss)