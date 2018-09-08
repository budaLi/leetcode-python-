#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/29
def countBinarySubstrings(s):
    """
    :type s: str
    :rtype: int
    """
    res=[]
    count=0
    for one in s:
        res.append(one)
        if res.count('0')>0 and res.count('1')>0:
            count+=1
            res.pop(0)

    return count
res=countBinarySubstrings("00110011")
print(res)