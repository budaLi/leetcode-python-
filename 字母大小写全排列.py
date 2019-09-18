# @Time    : 2019/9/17 18:43
# @Author  : Libuda
# @FileName: 字母大小写全排列.py
# @Software: PyCharm

class Solution(object):
    def __init__(self):
        """
        给定一个字符串S，通过将字符串S中的每个字母转变大小写，我们可以获得一个新的字符串。返回所有可能得到的字符串集合。

        示例:
        输入: S = "a1b2"
        输出: ["a1b2", "a1B2", "A1b2", "A1B2"]

        输入: S = "3z4"
        输出: ["3z4", "3Z4"]

        输入: S = "12345"
        输出: ["12345"]
        注意：

        S 的长度不超过12。
        S 仅由数字和字母组成。

        """

    def trans(self, s):
        """
        判断字符串是否为字母并进行大小转换
        :param s:
        :return:
        """
        if s.isalpha():
            if s.islower():
                s = s.upper()
            else:
                s = s.lower()
        return s

    def letterCasePermutation(self, S):
        """
        :type S: str
        :rtype: List[str]
        """
        res = [S]
        for one in S:
            one = self.trans(one)


if __name__ == "__main":
    S = Solution()
    s = "a1b2"
    res = S.letterCasePermutation(s)
    print(res)
