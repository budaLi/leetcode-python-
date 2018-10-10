#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/10/10
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def deleteNode(self, node):
        """
        :type node: ListNode
        :rtype: void Do not return anything, modify node in-place instead.
        """
        #4-3-1-5 要删除3
        #先变为 4-1-1-5
        #然后4-1-5
        node.val=node.next.val
        node.next=node.next.next