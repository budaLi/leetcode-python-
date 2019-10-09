# @Time    : 2019/10/9 16:39
# @Author  : Libuda
# @FileName: 分隔链表.py
# @Software: PyCharm

class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution(object):
    def __init__(self):
        """
        给定一个头结点为 root 的链表, 编写一个函数以将链表分隔为 k 个连续的部分。
        每部分的长度应该尽可能的相等: 任意两部分的长度差距不能超过 1，也就是说可能有些部分为 null。
        这k个部分应该按照在链表中出现的顺序进行输出，并且排在前面的部分的长度应该大于或等于后面的长度。
        返回一个符合上述规则的链表的列表。
        举例： 1->2->3->4, k = 5 // 5 结果 [ [1], [2], [3], [4], null ]。
        """

    def splitListToParts(self, root, k):
        """
        :type root: ListNode
        :type k: int
        :rtype: List[ListNode]
        """
        # 思路 第一遍遍历链表求出长度
        # 如果总长度小于K
        # 要求是 任意两部分的长度不超过1  前面部分的长度大于等于后面部分的长度。
