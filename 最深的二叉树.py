#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/13
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

def maxDepth(root):
    if root is None:
        print('null')
        return 0

    print(root.val)
    leftDepth=maxDepth(root.left)+1
    rightDepth=maxDepth(root.right)+1
    return maxab(leftDepth,rightDepth)

def maxab(a,b):
    if a>b:
        return a
    return b

node1=TreeNode(3)
node2=TreeNode(9)
node3=TreeNode(20)
node4=TreeNode(None)
node5=TreeNode(None)
node6=TreeNode(15)
node7=TreeNode(7)
node1.left=node2
node1.right=node3
node3.left=node6
node3.right=node7


res=maxDepth(node1)
print('Depth:',res)