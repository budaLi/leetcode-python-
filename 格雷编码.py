#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/10/10
class Solution(object):
    def grayCode(self, n):
        """
        :type n: int
        :rtype: List[int]
        """
        #找规律题
        #n=2时 [00,01,11,10]
        #当 n=3时 从n=2的最后一个元素开始向前移动 每次将最后一个元素末尾加0 同时将其加1 的结果加在列表后面
        #比如 从 n=2时的10 开始 末尾加0 变为 100 这个是在其本身改的 再加1 变为 101 加在列表末尾 此时列表为 {00，01，11，100，101】
        #第二次 [00,01,110,100,101,111]
        #第三次 [00,010,110,100,101,111,011]
        #最后一次 [000,010,110,100,101,111,011,001] 也就是只需变n-1次
        def trans(n):
            if n==1: return ['0','1']
            res=map(str,trans(n-1))
            tem=[]
            for j in range(-1,-len(res)-1,-1):
                tem.append(res[j]+'1')
                res[j]=res[j]+'0'
            res+=tem
            return res
        if n==0: return [0]
        return map(lambda x:int(x,2),trans(n))
#
# class Solution(object):       ?????
#     def binary_to_gray(self, num): # 从自然码变成格雷码的过程，利用数学公式
#         result =  num ^ (num >> 1)
#         return result
#
#     def grayCode(self, n):
#         """
#         :type n: int
#         :rtype: List[int]
#         """
#         # 首先遍历真实的数据
#         result = []
#         for i in range(2 ** n):
#             result.append(self.binary_to_gray(i))
#         return result
S=Solution()
res=S.grayCode(2)
print(res)
