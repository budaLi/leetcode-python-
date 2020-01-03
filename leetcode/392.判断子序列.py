# @Time    : 2020/1/3 9:57
# @Author  : Libuda
# @FileName: 392.判断子序列.py
# @Software: PyCharm
class Solution(object):
    def isSubsequence(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: bool
        """
        si = tj = 0
        while si < len(s) and tj < len(t):
            if s[si] == t[tj]:
                si += 1
                tj += 1
            else:
                tj += 1
        return si == len(s)


if __name__ == '__main__':
    S = Solution()
    s = "abc"
    t = "ahgdc" * 100
    res = S.isSubsequence(s, t)
    print(res)
