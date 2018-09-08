#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/7/24
class ListNode(object):   #节点
    def __init__(self):
        self.val=None
        self.next=None
class ListTale:           #链表
    def __init__(self):
        self.curnode=None
    def show(self):
        print('shownode')
        if  self.curnode:
            print(self.curnode.val)
            self.curnode=self.curnode.next
    def add(self,node):     #只能再当前节点添加
        if self.curnode:
            self.curnode.next=node
            if self.curnode.next:
                node.next=self.curnode.next
        self.curnode=node

    def reverse(self,listtable):
        list_tem=[]
        while listtable.curnode:
            list_tem.append(listtable.curnode.val)
            listtable.curnode=listtable.curnode.next
        temp=list(reversed(list_tem))
        listtable_new=ListTale()
        for tem in temp:
            node=ListNode()
            node.val=tem
            if listtable_new.curnode is None:
                listtable_new.curnode=node
            listtable_new.add(node)
            return listtable_new
    def twosum(self,list_table1,list_table2):
        list=ListTale()
        while list_table1.curnode and list_table2.curnode:
           tem=list_table1.curnode.val+list_table2.curnode.val
           node=ListNode()
           node.val=tem
           list.add(node)
           list_table1.curnode=list_table1.curnode.next
           list_table2.curnode=list_table2.curnode.next
        return list

list_tab1=ListTale()
list_tab2=ListTale()


node1=ListNode()
node1.val=3
node2=ListNode()
node2.val=4
node3=ListNode()
node3.val=2
node4=ListNode()
node4.val=4
node5=ListNode()
node5.val=6
node6=ListNode()
node6.val=5

list_tab1.add(node1)
list_tab1.add(node2)
list_tab1.add(node3)


list_tab2.add(node4)
list_tab2.add(node5)
list_tab2.add(node6)

list_tab1.show()

list3=ListTale()
