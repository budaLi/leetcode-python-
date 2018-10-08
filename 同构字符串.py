#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/10/9
def isIsomorphic(s, t):
    """
    :type s: str
    :type t: str
    :rtype: bool
    """
    if len(set(s))!=len(set(t)): return False
    t=list(t)
    dic={}
    for i in range(len(t)):
        if t[i] not in dic:
            dic[t[i]]=s[i]
            t[i]=s[i]
        else:
            t[i]=dic[t[i]]

    return ''.join(t)==s


res=isIsomorphic('foo','bqq')
print(res)
