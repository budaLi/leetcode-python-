#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/9/15
# def spilt(s):       #正则
#     import re
#     mat=re.compile('[a-zA-Z]')
#     res=re.findall(mat,s)
#     if res:
#         return ''.join(res)
#

def spilt(s):
    res=''
    for one in s:
        if (ord(one)>=65 and ord(one)<=90) or (ord(one)>=97 and ord(one)<=122):
            res+=one
    return res
res='asafboiwh8q80p[544*-*asd/a-sdasd'
res=spilt(res)
print(res)