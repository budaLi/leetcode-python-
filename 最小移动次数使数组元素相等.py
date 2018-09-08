#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/19
#给定一个长度为 n 的非空整数数组，找到让数组所有元素相等的最小移动次数。每次移动可以使 n - 1 个元素增加 1。
#这道题让每次移动n-1个数 每个数加1 也就是说 每次找到n-1 个数比第n个数小 来加 逆向思维是 每次找到最大的那个数减去1 直接每个数与最小值相等
#也就是 先找到min(nums)  然后对于每一个数都开始减去min(nums) 加起来就是需要移动的次数
#例如对于【1，2，3】 最小的数为 1 那么对于2，3 两个数每次减去1，需（2-1）+（3-1）+（1-1） 次 可变为 （2+3+1）- 1 *3 即所有数之和 减去 最小数*元素个数
def minMoves(nums):     #坑爹题
    #出奇制胜
    """
    :type nums: List[int]
    :rtype: int
    """
    sum=0
    for one in nums:
        sum=sum+one
    return sum-min(nums)*len(nums)



res=minMoves([1,2,3,4,4])
print(res)