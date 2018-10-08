#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/10/9
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution(object):
    def invertTree(self, root):
        """
        :type root: TreeNode
        :rtype: TreeNode
        """
        if root:
            head=root
            res=[head]
            while res:
                res[0].left,res[0].right=res[0].right,res[0].left
                node=res.pop(0)
                if node.left:
                    res.append(node.left)
                if node.right:
                    res.append(node.right)

        return root

