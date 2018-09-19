#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/9/19
def reverseStr(s, k):
    """
    :type s: str
    :type k: int
    :rtype: str
    """
    s=list(s)
    for i in range(0,len(s),2*k):
        s[i:i+k]=reversed(s[i:i+k])
    return ''.join(s)

res=reverseStr('abcdefg',2)
print(res)