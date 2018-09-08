#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/8/25
class treenode:
    def __init__(self,val):
        self.value=val
        self.left=None
        self.right=None

def avg(lis):
    num=0
    for one in lis:
        num+=one
    return num/float(len(lis))

def averageOfLevels(root):
    """
    :type root: TreeNode
    :rtype: List[float]
    """
    if root is None:
        return 0
    lis=[root]
    res=[]
    while lis:
        tem=[]
        for i in range(len(lis)):       #注意此处循环次数
            tem.append(lis[0].value)
            node=lis.pop(0)
            if node.left:
                lis.append(node.left)
            if node.right:
                lis.append(node.right)
        res.append(tem)

    return map(avg,res)

node1=treenode(1)
node2=treenode(2)
node3=treenode(3)


node1.left=node2
node1.right=node3

res=averageOfLevels(node1)
print(res)