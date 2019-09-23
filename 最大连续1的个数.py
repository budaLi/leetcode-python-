# @Time    : 2019/9/23 18:48
# @Author  : Libuda
# @FileName: 最大连续1的个数.py
# @Software: PyCharm

class Solution(object):
    def findMaxConsecutiveOnes(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        nums = map(str, nums)
        res = "".join(nums)
        res = res.split("0")
        le = 0
        for one in res:
            le = max(le, len(one))
        return le


if __name__ == "__main__":
    S = Solution()
    res = S.findMaxConsecutiveOnes([1, 1, 0, 1, 1, 1])
    print(res)
