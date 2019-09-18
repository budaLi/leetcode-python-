# @Time    : 2019/9/18 19:04
# @Author  : Libuda
# @FileName: 单调数列.py
# @Software: PyCharm

class Solution(object):
    def __init__(self):
        """
        如果数组是单调递增或单调递减的，那么它是单调的。
        如果对于所有 i <= j，A[i] <= A[j]，那么数组 A 是单调递增的。 如果对于所有 i <= j，A[i]> = A[j]，那么数组 A 是单调递减的。
        当给定的数组 A 是单调数组时返回 true，否则返回 false。
         
        示例 1：
        输入：[1,2,2,3]
        输出：true

        """

    def isMonotonic(self, A):
        """
        :type A: List[int]
        :rtype: bool
        """
        B = sorted(A)
        if B == A or B == A[::-1]:
            return True
        return False
