# @Time    : 2019/9/17 18:23
# @Author  : Libuda
# @FileName: Bigram分词.py
# @Software: PyCharm

class Solution(object):
    def __init__(self):
        """
        给出第一个词 first 和第二个词 second，考虑在某些文本 text 中可能以 "first second third" 形式出现的情况，其中 second 紧随 first 出现，third 紧随 second 出现。
        对于每种这样的情况，将第三个词 "third" 添加到答案中，并返回答案。

        示例 1：
        输入：text = "alice is a good girl she is a good student", first = "a", second = "good"
        输出：["girl","student"]

        示例 2：
        输入：text = "we will we will rock you", first = "we", second = "will"
        输出：["we","rock"]

        """
    def findOcurrences(self, text, first, second):
        """
        :type text: str
        :type first: str
        :type second: str
        :rtype: List[str]
        """
        res =[]
        text = text.split(" ")
        for i in range(len(text)-2):
            if text[i] == first:
                if text[i+1] == second:
                    res.append(text[i+2])
        return res

if __name__ == "__main__":
    S =Solution()
    text = "a a a a a a a a a"
    first = "a"
    second = "a"

    res = S.findOcurrences(text,first,second)
    print(res)