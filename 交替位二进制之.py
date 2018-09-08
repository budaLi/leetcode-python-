#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/26
def hasAlternatingBits(n):
    """
    :type n: int
    :rtype: bool
    """
    num=bin(n)[2:]
    print(num)
    num2=num[1:]
    for i in range(len(num2)):
        if num[i]==num2[i]:
            return False
    return True


res=hasAlternatingBits(5)
print(res)