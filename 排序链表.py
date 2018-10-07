#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/10/7
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


#垃圾办法 遍历链表 进行二分排序
class Solution(object):
    def sortList(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """
        lis=[]
        while head:
            lis.append(head.val)
            head=head.next
