#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/9/19
# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None

def removeElements(head, val):
    """
    :type head: ListNode
    :type val: int
    :rtype: ListNode
    """
    #需要存储第一个不是val的节点并最后返回
    pre_node = ListNode(None)
    pre_node.next = head
    q = pre_node
    while q.next:
        if q.next.val == val:
            q.next = q.next.next
        else:
            q = q.next


node1=ListNode(1)
node2=ListNode(2)
node3=ListNode(3)
node4=ListNode(4)
node5=ListNode(5)
node6=ListNode(6)

node1.next=node2
node2.next=node3
node3.next=node4
node4.next=node5
node5.next=node6

res=removeElements(node1,6)
while res:
    print(res.val)
    res=res.next
