#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/6
class ListNode():
    def __init__(self, x):
        self.val = x
        self.next = None
    def insert(self,node):
        if self is None:
            self=node
        else:
            self.next=node
            if self.next.next:
                node.next=self.next.next
class Solution(object):
    def mergeTwoLists(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        res=[]
        if l1 is None and l2 is not None:
            return l2
        if l2 is None and l1 is not None:
            return l1
        if l1 is None and l2 is None:
            return None
        if l1 and l2:
            while l1:
                res.append(l1.val)
                l1=l1.next
            while l2:
                res.append(l2.val)
                l2=l2.next
            res.sort()
        node=ListNode(0)
        tem=ListNode(0)
        for i in range(len(res)):
            if i==0:
                node.val=res[i]
                tem=node
            else:
                next_node=ListNode(res[i])
                node.insert(next_node)
                node=next_node

        return tem
node1=ListNode(1)
node2=ListNode(2)
node3=ListNode(4)
node4=ListNode(1)
node5=ListNode(3)
node6=ListNode(4)

node1.next=node2
node2.next=node3

node4.next=node5
node5.next=node6

S=Solution()
res=S.mergeTwoLists(node1,node4)
print(res.val)