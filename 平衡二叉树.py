#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/25
class tree:
    def __init__(self,val):
        self.val=val
        self.left=None
        self.right=None
    def not_is_None(self):
        if self is None:
            return False
        else:
            return True
    def is_leaf(self):
        if self.not_is_None() and (self.left or self.right):
            return False
        else:
            return True
    def has_lchild(self):
        if self.not_is_None() and self.left:
            return True
        else:
            return False
    def has_right(self):
        if self.not_is_None() and self.right:
            return True
        else:
            return False
    def has_all_child(self):
        if self.has_lchild() and self.has_right():
            return True
        else:
            return False
    def has_any_child(self):
        if self.is_leaf():
            return False
        else:
            return True
def get_wight(node):
    if node is None:
        return 0
    else:
        return abs(get_x(node.left)-get_x(node.right))

def get_x(root):
    if root is None :
        return 0
    elif root.has_any_child():
        if root.has_all_child():
            return max(get_x(root.left),get_x(root.right))+1
        elif (root.has_lchild() and not root.right):
            return get_x(root.left)+1
        else:
            return get_x(root.right)+1
    else:   #叶子
        return 1
def isBalanced(root):
    """
    :type root: TreeNode
    :rtype: bool
    """
    while root:
        if get_wight(root)>1:
            return False
        return isBalanced(root.left) and isBalanced(root.right)

    return True


node1=tree(1)
node2=tree(2)
node3=tree(3)
node4=tree(4)
node5=tree(5)


node1.left=node2
node1.right=node3
node2.left=None
node2.right=None
node4.left=node4
node3.right=node5


# gg=isBalanced(node1)
# print(gg)
x=isBalanced(node1)
print(x)