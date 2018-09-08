#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/9/2
#修建二叉搜索树
#运用递归的思想 如果这个结点符合则次结点为根节点 对它的左自述得和右子树递归
#如果小于L 说明这个结点的左子树已经不满足 递归其右子树
#如果大于R  说明这个结点右子树不满足 递归左子树
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

def trimBST(root, L, R):
    """
    :type root: TreeNode
    :type L: int
    :type R: int
    :rtype: TreeNode
    """
    if root is None:
        return None
    elif root.val<L:
        return trimBST(root.right,L,R)
    elif root.right>R:
        return trimBST(root.left,L,R)
    root.left=trimBST(root.left,L,R)
    root.right=trimBST(root.right,L,R)
    return root


node1=TreeNode(1)
node2=TreeNode(0)
node3=TreeNode(2)

node1.left=node2
node1.right=node3

res=trimBST(node1,1,2)
print(res)
