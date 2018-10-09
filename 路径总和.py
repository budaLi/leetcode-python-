#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/10/9
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

#超过了2/3 的人 另外一种思路是 通过递归 好像比较快。。。
class Solution(object):
    def hasPathSum(self, root, sums):
        """
        :type root: TreeNode
        :type sum: int
        :rtype: bool
        """
        #思路 存储每个节点对应的到sums的距离 即从根节点开始到这个节点和sums的差值
        #如果这个节点 所对应的值为0 说明从根节点开始到这个节点的和为 sums 同时如果这个节点为根节点 返回true
        if root is None: return False
        res=[root]
        dic={}
        dic[root]=sums-root.val
        while res:
            node=res.pop(0)
            if node.left:
                res.append(node.left)
                dic[node.left]=dic[node]-node.left.val
            if node.right:
                res.append(node.right)
                dic[node.right]=dic[node]-node.right.val
        for one in dic:
            if dic[one]==0 and not one.left and not one.right:
                return True
        return False

