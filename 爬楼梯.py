#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/8
#斐波那契数列解决爬楼梯问题


# def climbStairs(n):     #递归会超出时间限制
#     if n<0:
#         return False
#     if n==1:
#         return 1
#     if n==2:
#        return 2
#     else:
#         res=climbStairs(n-1)+climbStairs(n-2)
#         return res
def climbStairs(n): #利用列表存储斐波那契数列的前几个数，往后加
    res=[1,2]
    for i in range(2,n):
        res.append(res[i-1]+res[i-2])
    return res[n-1]
res=climbStairs(35)
print(res)