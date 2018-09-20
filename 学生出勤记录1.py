#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/9/20
def checkRecord(s):
    """
    :type s: str
    :rtype: bool
    """
    #不超过两个连续的L 可以判断LLL没有出现
    if s.count('A')<=1 and s.count('LL')<1:
        return True
    return False

tem='PPALLL'
res=checkRecord(tem)
print(tem.count('LL'))
print(res)