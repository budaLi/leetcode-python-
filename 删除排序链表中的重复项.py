#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/9
class ListNode(object):
    def __init__(self,x):
        self.val=x
        self.next=None
    def insert(self,node):
        self.next=node
class Solution(object):
    # def deleteDuplicates(self,head):  #利用列表存储链表结点
    #     d=[]
    #     while head:
    #         if head.val not in d:
    #            d.append(head.val)
    #         head=head.next
    #     head=listnode=ListNode(0)
    #     for index in range(len(d)):
    #         if index==0:
    #             listnode.val=d[0]
    #         else:
    #             listnode_new=ListNode(d[index])
    #             listnode.next=listnode_new
    #             listnode=listnode_new
    #     return head
    def deleteDuplicates(self,head):
        if head is None:        #利用链表本身
            return None
        res=head
        while head.next:
            if head.val==head.next.val:
                head.next=head.next.next
            else:
                head=head.next
        return res


listnode1=ListNode(1)
listnode2=ListNode(1)
listnode3=ListNode(2)
listnode4=ListNode(2)
listnode5=ListNode(3)

listnode1.next=listnode2
listnode2.next=listnode3
listnode3.next=listnode4
listnode4.next=listnode5

S=Solution()
res=S.deleteDuplicates(listnode1)
print(res.next.next.val)

