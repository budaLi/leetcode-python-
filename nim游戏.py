#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/9/11
#写出前几种情况 发现4的倍数不能赢
def canWinNim(n):
    """
    :type n: int
    :rtype: bool
    """
    if n%4==0: return False
    return True

res=canWinNim(1348820612)
print(res)