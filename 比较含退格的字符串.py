#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/8/25
def backspaceCompare( S, T):
    """
    :type S: str
    :type T: str
    :rtype: bool
    """
    if rep(S)==rep(T):
        return True
    else:
        return False
def rep(res):
    import re
    mat=re.compile('[a-z]{1}#{1}')
    tem=re.findall(mat,res)
    while tem:
        for one in tem:
            res=res.replace(one,'')
        tem=re.findall(mat,res)
    res=res.replace('#','')
    return res

res=backspaceCompare("ab##",        #这种情况比较特殊
"c#d#")
print(res)