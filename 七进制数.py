#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/26
def convertToBase7(num):
    """
    :type num: int
    :rtype: str
    """
    res=[]
    flag=''
    if num ==0:
        return '0'
    if num<0:
        num=abs(num)
        flag='-'
    while num/7.0!=0:
        shang,yushu=num/7,num%7
        res.append(str(yushu))
        num=shang
    return flag+''.join(res[::-1])

num=-7
res=convertToBase7(num)
print(res)