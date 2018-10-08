#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/10/8
# def integerBreak(n):
#     """
#     :type n: int
#     :rtype: int
#     """
#     #win10卡死已经把我心态搞炸 这个递归的方法虽然可以通过测试用例 但是慢的出天际
#     if n==1: return 1
#     if n<=3: return n-1
#     #对于一个大于3的数可以存在多种分解 我们需要求最大值
#     return max(2*integerBreak(n-2) if n-2>3 else 2*(n-2),3*integerBreak(n-3) if n-3>3 else 3*(n-3))


#范例思路 发现当n>4时 将数字每次按3分乘积最大
#如 5 = 2*3 6=3*3 7=3*4 8=3*3*2 9=3*3*3 10=3*3*4
def integerBreak(n):
    if n<=3: return n-1
    res=1
    while n>4:
        res*=3
        n-=3
    return res*n    #n小于4时直接*
res=integerBreak(10)
print(res)
