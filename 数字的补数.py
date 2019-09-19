# @Time    : 2019/9/19 13:06
# @Author  : Libuda
# @FileName: 数字的补数.py
# @Software: PyCharm

class Solution(object):
    def __init__(self):
        """
        给定一个正整数，输出它的补数。补数是对该数的二进制表示取反。
        注意:
        给定的整数保证在32位带符号整数的范围内。
        你可以假定二进制数不包含前导零位。
        示例 1:
        输入: 5
        输出: 2
        解释: 5的二进制表示为101（没有前导零位），其补数为010。所以你需要输出2。
        """

    def findComplement(self, num):
        """
        :type num: int
        :rtype: int
        """
        # print(~num)  #按位取反 相当于-x-1  5:0101->1010
        s = str(int(bin(num)[2:]))
        tem = int("".join(["1"] * len(s)))
        res = num ^ int(str(tem), 2)
        return res


if __name__ == "__main__":
    S = Solution()
    res = S.findComplement(8)
    print(res)
