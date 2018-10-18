#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/10/3

#回文素数   还是超出时间限制

#从这个数开始逐个加一判断这个数是否是回文数 和 素数 满足返回
def primePalindrome(N):
    """
    :type N: int
    :rtype: int
    """
    def is_sushu(n):    #判断是否是素数
        if n==1: return False
        for i in range(2,n/2+1):
            if n%i==0:
                return False
        return True

    def is_huiwen(n):   #回文
        return str(n)[::-1]==str(n)

    tem=N
    while 1:
        if is_huiwen(tem) and is_sushu(tem):
            return tem
        else:
            print(tem)
            if len(str(tem))<=2:
                tem+=1
                continue
            if len(str(tem)) %2==0: #偶数位数变为奇数
                tem=int('1'+'0'*len(str(tem)))
            else:   #如果是奇数位将后面的数字对应变为前面的数
                tem=list(str(tem))
                for i in range(-1,-len(tem)/2-1,-1):
                    tem[i]=tem[-i-1]
                tem=int(''.join(tem))   #变为回文数
                if is_sushu(tem) and tem>N: return tem
                else:   #此时为回文数 在除最高位的其他位数逐渐加 而不是只加一
                    tem+=int('1'+'0'*(len(str(tem))/2))  #例如10000 10101 10201 10301这种变化
# for i in range(1,10000):    #发现除11外 所有满足条件的数 位数均为奇数
#     res=primePalindrome(i)
#     print(res)

#7519158
res=primePalindrome(9989900)
print(res)
