#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/9/19

# def repeatedSubstringPattern(s):
#     """
#     :type s: str
#     :rtype: bool
#     """
#     tem=''
#     length=len(s)
#     for one in s[:-1]:
#         tem+=one
#         print(tem)
#         if length%len(tem)!=0: continue
#         if s.replace(tem,'')=='': return True   #全部替换如果为空则True
#     return False


#范例
def repeatedSubstringPattern(s):
    """
    :type s: str
    :rtype: bool
    """
    if not s or len(s) < 2:
        return False

    strlen = len(s)
    pos = strlen / 2
    while pos > 0:
        if strlen % pos == 0:
            substr = s[:pos]
            divisor = strlen / pos
            if substr*divisor == s:
                return True
        pos -= 1
    return False

#先提取字符串的一半，然后乘以2，看生成串和原串是否相同，相同则true，
# 否则提取字符串三分之一，然后乘以3，以此类推。其实思路和上面大同小异，
#但是利用python的这个特性省去了好多麻烦，还缩短了运行时间
res=repeatedSubstringPattern("abcabcabcabc")
print(res)

