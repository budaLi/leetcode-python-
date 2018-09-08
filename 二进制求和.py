#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/8
# def addBinary(a, b):        #繁琐
#     if a =='' or b== "":
#         return a+b
#     if len(a)<len(b):   #a作为被加数
#         tem=a
#         a=b
#         b=tem
#     a=list(map(int,list(reversed(a))))
#     b=list(map(int,list(reversed(b))))
#     for i in range(len(a)-len(b)):
#         b.append(0)
#     res=[0 for i in range(len(a))]
#     flag=0
#     for i in range(len(a)):
#         res[i]=(a[i]+b[i]+flag)%2
#         flag=int((a[i]+b[i]+flag)/2)
#     if flag==1:
#         res.append(1)
#     res=list(reversed(res))
#     res=list(map(str,list(res)))
#     print(res)
#     ans="".join(res)
#     return ans


def addBinary(a, b):    #bin函数，返回一个整数 int 或者长整数 long int 的二进制表示。
                            #  int(a,b) 将一个字符串或数字以指定进制输入，十进制输出
    res=int(a,2)+int(b,2)
    return bin(res)[2:]     #由于输出以0b开头 所以切片

res=addBinary('11','1')
print(res)
# l = ["hi","hello","world"]
# print(" ".join(l))
