#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/9/6
def judgeSquareSum(c):
    """
    :type c: int
    :rtype: bool
    """
    import math
    a=0
    b=int(math.sqrt(c))
    for i in range(b+1):
        if a**2+b**2<c: a+=1
        elif a**2+b**2>c: b-=1
        elif a**2+b**2==c: return True
    return False
res=judgeSquareSum(2)
print(res)