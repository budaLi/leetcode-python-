#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/8/26
def maxProfit(prices):
    """
    :type prices: List[int]
    :rtype: int
    """
    res=0
    for i in range(len(prices)):
        if prices[0] ==max(prices):
            prices=prices[1:]
            continue
        else:
            res=max(max(prices)-prices[0],res)
            prices=prices[1:]
    return res
res=maxProfit([10,9,8,5,4,2,1])
print(res)

print(float('inf')) #正无穷
print(float('-inf'))
