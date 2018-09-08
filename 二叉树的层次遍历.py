#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/14
# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution(object):
    def levelOrderBottom(self, root):
        """
        :type root: TreeNode
        :rtype: List[List[int]]
        """
        if not root:return []         #answer
        s = [root]
        res=[]
        while s:
            l=[]
            for i in range(len(s)):
                n = s.pop(0)
                l.append(n.val)
                if n.left:
                    s.append(n.left)
                if n.right:
                    s.append(n.right)
            res.append(l)
        return res[::-1]

node1=TreeNode(3)
node2=TreeNode(9)
node3=TreeNode(20)
node4=TreeNode(15)
node5=TreeNode(7)
node6=TreeNode(10)
node7=TreeNode(6)

node1.left=node2
node1.right=node3
node3.left=node4
node3.right=node5
node2.left=node6
node6.left=node7

S=Solution()
res=S.levelOrderBottom(node1)
print(res)

# A=[3]
# c=[3,4]
# A=[A]
# A.append(c)
# print(A)


# A=[1,2,3]
# for i in range(len(A)): #以后修改A的长度以后再循环 这里只循环A的初始长度
#     print(i)
#     A.append(i**2)
# print(A)