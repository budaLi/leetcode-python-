#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/8
def lengthOfLastWord(s):
    s=s.strip()         #去除两边的空格 避免'','    '，这种情况无法正确处理
    if s=='':
        return 0
    s=s.split()
    return len(s[-1])
s='ss sss'
res=lengthOfLastWord(s)
print(res)

