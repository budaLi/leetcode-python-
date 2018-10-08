#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/10/8
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution(object):
    def getIntersectionNode(self, headA, headB):
        """
        :type head1, head1: ListNode
        :rtype: ListNode
        """
        #直接思路 遍历两个链表求相同的值的区域
        lis1=[]
        lis2={}
        while headA:
            lis1.append(headA.val)
            headA=headA.next
        while headB:
            lis2[headB.val]=1
            headB=headB.next
        for one in lis1:
            if one in lis2:
                node=ListNode(one)
                return node
        return None
