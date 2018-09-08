#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/8/31
#未解决
class TreeNode(object):
    def __init__(self,val):
        self.val=val
        self.left=None
        self.right=None

class Solution(object):
    def longestUnivaluePath(self, root):
        """
        :type root: TreeNode
        :rtype: int
        """
        if root is None:
            return 0
        res=[root]
        count=[]
        while res:
            if res[0].left:
                if res[0].val==res[0].left.val:
                    count.append(self.get_val(res[0].left)+1)
                else:
                    count.append(self.get_val(res[0].left))
            if res[0].right:
                if res[0].val==res[0].right.val:
                    count.append(self.get_val(res[0].right)+1)
                else:
                    count.append(self.get_val(res[0].right))
            else:
                return 0
            node=res.pop(0)
            if node.left:
                res.append(node.left)
            if node.right:
                res.append(node.right)
        if count:
            return max(count)
    def get_val(self,root):
        if root is None:
            return 0
        count=0
        if not root.left and not root.right:
            return 0
        elif root.left and not root.right:
            if root.left.val==root.val:
                count+=1
        elif root.right and not root.left:
            if root.right.val==root.val:
                count+=1
        else:
            return max(self.get_val(root.left),self.get_val(root.right))
        return count


node1=TreeNode(1)
node2=TreeNode(2)
node3=TreeNode(3)
node4=TreeNode(2)
node5=TreeNode(4)
node6=TreeNode(5)

node1.left=node2
node1.right=node3
node2.right=node4
node3.left=node5
node3.right=node6

S=Solution()
res=S.longestUnivaluePath(node1)

print(res)