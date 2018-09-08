#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/26
def binaryGap(N):
    """
    :type N: int
    :rtype: int
    """
    num=bin(N)[2:]
    if num.count('1')<=1:
        return 0
    res=[]
    for i in range(len(num)):
        if num[i]=='1':
            res.append(i)
    tem=[]
    for i in range(len(res)-1):
        tem.append(res[i+1]-res[i])
    return max(tem)

res=binaryGap(8)
print(res)