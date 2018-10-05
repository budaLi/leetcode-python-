#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/10/5
def countPrimeSetBits(L, R):
    """
    :type L: int
    :type R: int
    :rtype: int
    """
    import math
    def is_zhishu(num):
        if num==1: return 0
        for i in range(2,int(math.sqrt(num))+1):
            if num%i==0:
                return 0
        return 1
    res=0
    for i in range(L,R+1):
        tem = bin(i).count('1')
        print(tem)
        res+=is_zhishu(tem)
    return res

res=countPrimeSetBits(L = 6, R = 10)
print(res)
