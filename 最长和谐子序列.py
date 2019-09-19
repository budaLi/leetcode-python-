# @Time    : 2019/9/19 9:36
# @Author  : Libuda
# @FileName: 最长和谐子序列.py
# @Software: PyCharm
class Solution(object):
    def __init__(self):
        """
        和谐数组是指一个数组里元素的最大值和最小值之间的差别正好是1。
        现在，给定一个整数数组，你需要在所有可能的子序列中找到最长的和谐子序列的长度。
        示例 1:
        输入: [1,3,2,2,5,2,3,7]
        输出: 5
        原因: 最长的和谐数组是：[3,2,2,2,3].
        """

    def findLHS(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        dic = {}
        for one in nums:
            if one not in dic:
                dic[one] = 1
            else:
                dic[one] += 1

        # tem = sorted(dic)
        # res = []
        # for key in tem:
        #     if key + 1 in dic:
        #         res.append(dic[key + 1] + dic[key])
        # #此处要注意 [1,1,1,1]这种可能使res长度为0的形式
        # if len(res)!=0:
        #     return max(res)
        # return 0

        # 优化
        res = 0
        for key in dic:
            if key + 1 in dic:
                res = max(res, dic[key + 1] + dic[key])
        return res


if __name__ == "__main__":
    S = Solution()
    nums = [1, 3, 2, 2, 5, 2, 3, 7]
    res = S.findLHS(nums)
    print(res)
