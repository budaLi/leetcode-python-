#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/5
#判断一个数字是不是回文数，我们可以将其反转与原来比较，负数肯定不是回文数
def is_huiwen(num):
    if num<0:
        return False    #负数肯定不是
    res=0
    tem=num             #用来存储输入的数
    while(num!=0):      #将数字反转
        res=res*10+num%10
        num=int(num/10)
    if res==tem:
        return True
    else:
        return False

res=is_huiwen(12321)
print(res)