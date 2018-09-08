#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/27
def toLowerCase(strs):
    """
    :type str: str
    :rtype: str
    """
    res=''
    for i in range(len(strs)):
        if ord(strs[i])>=65 and ord(strs[i])<=90:
            res+=chr(ord(strs[i])+32)
            continue
        res+=strs[i]
    return res

res=toLowerCase('Helll')
print(res)