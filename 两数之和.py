# @Time    : 2019/9/20 10:16
# @Author  : Libuda
# @FileName: 两数之和.py
# @Software: PyCharm

class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        dic = {}
        for index, values in enumerate(nums):
            if target - values in dic:
                return [dic[target - values], index]
            dic[values] = index


if __name__ == "__main__":
    S = Solution()
    nums = [2, 7, 11, 15]
    target = 9
    res = S.twoSum(nums, target)
    print(res)
