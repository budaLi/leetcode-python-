#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/8

# def mySqrt(x):      #垃圾方法
#     min=0
#     max=x
#     mid=0
#     while min<max:
#         mid=int((min+max)/2)
#         if  mid**2==x:
#             return mid
#         if  mid**2<x:
#             if (mid+1)**2>x:
#                 return mid
#             if (mid+1)**2==x:
#                 return mid+1
#             min=mid
#         else:
#             max=mid
#     if min >1:
#         return min-1
#     return min
def mySqrt(x):  #牛顿迭代法
    result = 1.0
    tem=0
    if result * result - x<0: tem=-(result * result - x)
    else:tem=result * result - x
    while tem > 0.1:
        result = (result + x / result) / 2
        if result * result - x<0: tem=-(result * result - x)
        else:tem=result * result - x
    return int(result)
res=mySqrt(14)
print(res)