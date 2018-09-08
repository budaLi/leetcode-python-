#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/5
import sys
import math
max_int=2**31-1
min_int=-(max_int+1)


def tran(num):
    flag=0
    if num<0:
        flag=1
        num=abs(num)
    if num<min_int or  num>max_int:
        return 0
    res=0
    while(num!=0):
        res=res*10+num%10
        num=int(num/10)
        print(res,num)
        if res<min_int or res>max_int:
            return 0
    if flag==1:
        return -res
    else:
        return res
print(max_int)
res=tran(1534236469)
print(res)