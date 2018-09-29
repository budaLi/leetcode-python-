#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/9/29
#遍历 符合条件则输出
def readBinaryWatch(num):
    """
    :type num: int
    :rtype: List[str]
    """
    res=[]
    for i in range(12):
        for j in range(60):
            if (bin(i)+bin(j)).count('1')==num:
                res.append('%d:%02d'%(i,j)) #%02d 表示不够两位用0补
    return res


res=readBinaryWatch(1)
print(res)