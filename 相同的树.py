#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/9
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

#
# tem1=[]
# def inorderp(p):
#     if p:
#         tem1.append(p.val)
#         inorderp(p.left)
#         inorderp(p.right)
#     elif p and p.left is None and p.right is None:
#         tem2.append(p.val)
#     return tem1
#
# tem2=[]
# def inorderq(q):
#     if q and  (q.left or q.right):
#         tem2.append(q.val)
#         inorderq(q.left)
#         inorderq(q.right)
#     elif q  and q.left is None and q.right is None:
#         tem2.append(q.val)
#     return tem2


def isSameTree(p,q):
    if p is None and q is None:
        return True
    elif p and q:
        if p.val!=q.val:
            return False
        else:
             return (isSameTree(p.left,q.left) and isSameTree(p.right,q.right))
    else:
        return False


node1=TreeNode(1)
node2=TreeNode(2)
node3=TreeNode(1)

node1.left=node2
node1.right=node3

node4=TreeNode(1)
node5=TreeNode(2)
node6=TreeNode(1)

# node4.left=node5
node4.right=node6


res=isSameTree(node1,node4)
print(res)