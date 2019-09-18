# @Time    : 2019/9/18 19:11
# @Author  : Libuda
# @FileName: 气球的最大数量.py
# @Software: PyCharm

class Solution(object):
    def __init__(self):
        """
        给你一个字符串 text，你需要使用 text 中的字母来拼凑尽可能多的单词 "balloon"（气球）。
        字符串 text 中的每个字母最多只能被使用一次。请你返回最多可以拼凑出多少个单词 "balloon"。
        示例 1：
        输入：text = "nlaebolko"
        输出：1
        """

    def maxNumberOfBalloons(self, text):
        """
        :type text: str
        :rtype: int
        """
        dic = {}
        for one in text:
            if one not in dic:
                dic[one] = 1
            else:
                dic[one] += 1

        res = min(dic.get("b", 0), dic.get("a", 0), int(dic.get("l", 0) / 2), int(dic.get("o", 0) / 2), dic.get("n", 0))
        return res


if __name__ == "__main__":
    S = Solution()
    text = "loonbalxballpoon"
    res = S.maxNumberOfBalloons(text)
    print(res)
