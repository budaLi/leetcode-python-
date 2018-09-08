#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/19
def hammingWeight(n):   #转为2进制 count
    res=(bin(n)).count('1')
    return res


res=hammingWeight(2)
print(res)