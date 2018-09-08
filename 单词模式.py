#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/15

#技巧 当两个字符串模式完全匹配时 他们的长度相等且去重后长度依然相等
class Solution(object):
    def wordPattern(self, pattern, str):
        """
        :type pattern: str
        :type str: str
        :rtype: bool
        """
        #使用字典，pattern当key,str当value，形成配对
        # dic = {}
        # strToList= str.split()
        # if len(pattern) != len(strToList) or len(set(pattern)) != len(set(strToList)):
        #     return False
        # for i in range(len(pattern)):   #i取str val取pattern
        #     if pattern[i] not in dic:
        #         dic[pattern[i]] = strToList[i]
        #     elif dic[pattern[i]] != strToList[i]:
        #         return False
        # return True


        # a=str.split(' ')      #zip组合两个列表后再次去重长度一样
        # if len(pattern)!=len(a):
        #     return False
        # else:
        #     if len(set(pattern))==len(set(a))==len(set(zip(pattern,a))):
        #         return True
        #     else:
        #         return False

S=Solution()
res=S.wordPattern('abba','dog m m dog')
print(res)