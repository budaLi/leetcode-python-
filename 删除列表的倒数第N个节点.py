#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/9/22
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution(object):
    def removeNthFromEnd(self, head, n):
        """
        :type head: ListNode
        :type n: int
        :rtype: ListNode
        """
        pre=ListNode(None)
        pre.next=head
        las=ListNode(None)
        las.next=head
        count=0
        while pre:
            if count<n:
                head=head.next
                count+=1
            else:
                las=las.next
                head=head.next
