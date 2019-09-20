# @Time    : 2019/9/20 11:12
# @Author  : Libuda
# @FileName: 最常见的单词.py
# @Software: PyCharm
class Solution(object):
    def mostCommonWord(self, paragraph, banned):
        """
        :type paragraph: str
        :type banned: List[str]
        :rtype: str
        """
        dic = {}
        paragraph = self.splitParagraph(paragraph)
        print(paragraph)
        for one in paragraph:
            if one in banned:
                pass
            elif one not in dic:
                dic[one] = 1
            else:
                dic[one] += 1
        # dic= sorted(dic.items(),key = lambda key:key[1],reverse=True)
        tem = max(dic.values())
        for key, value in dic.items():
            if value == tem:
                return key

    def splitParagraph(self, paragraph):
        s = ['!', '?', "'", ",", ";", "."]
        for one in s:
            paragraph = paragraph.replace(one, " ")
        paragraph = paragraph.lower().split()
        return paragraph


if __name__ == "__main__":
    S = Solution()
    paragraph = "Bob hit a ball, the hit BALL flew far after it was hit."
    banned = ["hit"]
    res = S.mostCommonWord(paragraph, banned)
    # res= S.splitParagraph(paragraph)
    print(res)
