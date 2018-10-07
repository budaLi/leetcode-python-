#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/10/5
def checkPerfectNumber(num):
    """
    :type num: int
    :rtype: bool
    """
    res=0
    if num<=1: return False
    import math
    for i in range(2,int(math.sqrt(num))+1):
        if num%i==0:
            res+=i+num/i
    print(res)
    return res+1==num

res=checkPerfectNumber(6)
print(res)