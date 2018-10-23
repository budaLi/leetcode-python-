#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/10/23
#【1，2，3，5，8，13]

class Solution:
    def rectCover(self, number):
        # write code here
        dic={1:1,2:2}
        for i in range(3,number+1):
            dic[i]=dic[i-1]+dic[i-2]
        print(dic)
        return dic[number]

S=Solution()
res=S.rectCover(1)
print(res)