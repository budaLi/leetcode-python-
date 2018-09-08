#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/1

#除法比乘法耗费时间
#特殊情况：x不属于【-100.0，100.0】,n不属于【-min_int,max_int】且x！=1 and x!=-1
            #时间问题通过二分法且尽量用乘法可以解决
import sys
import math
print(sys.maxsize)  #最大整数为2^63-1
max_int=int(math.sqrt((sys.maxsize+1)*2)/2-1)   #2^31-1
min_int=-(max_int+1)        #2^-31
print(max_int)
print(min_int)
def mypow(x,n):     #自己写的垃圾代码
    if x<=-100.0 or x>=100.0 or (n<=min_int and x!=1 and x!=-1) or (n>=max_int and x!=1 and x!=-1) or (x>0 and x<1 and n>=max_int):
        return 0
    if x==0:
        if n>0:
            return 0
        else:
            return False
    elif x==1:
        return 1
    elif x==-1:
        if n%2==0:
            return 1
        else:
            return -1
    elif n==1:
        return x
    elif n>0:   #n>0
        if n%2==0:  #n为偶数
            return mypow(x,n/2)*mypow(x,n/2)
        else:       #n为奇数
            n=int(n/2)
            return (mypow(x,n)*mypow(x,n))*x
    elif n<0:
        n=abs(n)    #取绝对值
        if n%2==0:  #n为偶数
            return 1/(mypow(x,n/2)*mypow(x,n/2))
        else:       #n为奇数
            n=int(n/2)
            return 1/((mypow(x,n)*mypow(x,n))*x)
    elif n==0:
        return 1

# def best_pow(x,n):    #leetcode上范例代码
#     if n<0:
#         x = 1/x
#         n = -n
#     res = 1
#     while n>0:
#         if n&1:
#             res *= x
#         x *= x
#         n >>=1
#     return res


import datetime
start=datetime.datetime.now()
x=mypow(-0.99999,
933520)
print(x)
end=datetime.datetime.now()
print(end-start)

start=datetime.datetime.now()
print(pow(-0.99999,
933520))
end=datetime.datetime.now()
print(end-start)
