#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/26
import re
def calPoints(ops):
    """
    :type ops: List[str]
    :rtype: int
    """
    res=[]
    for one in ops:
        if re.match('.*[0-9]+',one):
            res.append(int(one))
        elif one =='C':
            res.pop()
        elif one =='D':
            res.append(res[-1]*2)
        elif one == '+':
            res.append(res[-1]+res[-2])
        print(res)

    return sum(res)

res=calPoints(["5","-2","4","C","D","9","+","+"])
print(res)