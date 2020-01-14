# @Time    : 2020/1/14 11:20
# @Author  : Libuda
# @FileName: 找出二叉搜索树第二大的树.py
# @Software: PyCharm

class Tree:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def Solution(root):
    if root:
        if root.right:
            if root.right.right:
                return Solution(root.right)
            elif root.right.left:
                return root.right.left.val
            return root.val
        elif root.left:
            return root.left.val
    return None


root = Tree(20)
lv1_1 = Tree(15)
lv1_2 = Tree(25)
lv2_1 = Tree(4)
lv2_2 = Tree(18)
lv2_3 = Tree(23)
lv2_4 = Tree(60)

root.left, root.right = lv1_1, lv1_2
lv1_1.left, lv1_1.right = lv2_1, lv2_2
lv1_2.left, lv1_2.right = lv2_3, lv2_4

res = Solution(root)

print(res)
