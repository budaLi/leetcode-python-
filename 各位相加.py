#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/20
# def addDigits(num):     #垃圾方法
#     tem=str(num)
#     if len(tem)==1:
#         return num
#     while len(tem)>1:
#         res=0
#         for one in tem:
#             res=res+int(one)
#         tem=str(res)
#     return int(tem)


def addDigits(num):
    """
    :type num: int
    :rtype: int
    """
    print(num % 9 or 9)
    print(9 and 18)
    return num and (num % 9 or 9)

res=addDigits(18)
print('result',res)