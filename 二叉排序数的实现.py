#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/8/1
class TreeNode(object): #二叉树

    def __init__(self,data=None,parent=None,lchild=None,rchild=None):
        self.data=data
        self.parent=parent
        self.lchild=lchild
        self.rchild=rchild

    def has_parent(self):   #是否有双亲
        if self.parent:
            return True
        else:
            return False
    def has_lchild(self):   #是否有左子树
        return self.lchild

    def has_rchild(self):   #是否有右子树
        return self.rchild

    def has_any_child(self):    #是否有子树
        return self.lchild or self.rchild

    def has_both_child(self):   #是否有左右子树
        return self.lchild and self.rchild

    def is_lchild(self):    #是否是左子树
        if self.parent and self.parent.lchild==self:
            return True
        return False

    def is_rchild(self):
        if self.parent and self.parent.rchild==self:  #是否是右子树
            return True
        return False

    def is_leaf(self):  #是否是叶子
        return not (self.lchild or self.rchild)

    def is_root(self):
        return not self.parent

def search(treenode,key):   #搜索值返回树的结点
    if treenode.data==key:
        return treenode
    elif key<treenode.data:
        if treenode.has_lchild():
            return search(treenode.lchild,key)
        else:
            return None
    elif key>treenode.data:
        if treenode.has_rchild():
            return search(treenode.rchild,key)
        else:
            return None
    else:
        return None


def get_min_lchild(treenode):   #获取最小的左子树的结点
    if treenode and treenode.has_lchild():
        return get_min_lchild(treenode.lchild)
    elif treenode and treenode.is_leaf():
        return treenode
    else:
        return None

def get_min_rchild(treenode):   #获取最小的右子树的结点
    if treenode and treenode.has_rchild():
        return get_min_lchild(treenode.rchild)
    elif treenode and treenode.is_leaf():
        return treenode
    else:
        return None

def insert(treenode,key):   #插入 当结点为空时插入
    if treenode.data is None:
        treenode.data=key
        print('插入成功')
    if treenode.data==key:
        print('该值已经存在,插入失败')
    elif key<treenode.data:
        print('<')
        if treenode.has_lchild():
            return insert(treenode.lchild,key)
        else:
            new_node=TreeNode(key,treenode,None,None)
            treenode.lchild=new_node
            print('插入成功')
    elif key>treenode.data:
        print('>')
        if treenode.has_rchild():
            return insert(treenode.rchild,key)
        else:
            new_node=TreeNode(key,treenode,None,None)
            treenode.rchild=new_node
            print('插入成功')

def depth_first_show(treenode):     #深度优先遍历二叉树
    if treenode:
        print(treenode.data)
        depth_first_show(treenode.lchild)
        depth_first_show(treenode.rchild)


def width_first_show(treenode): #广度优先遍历 队列实现
    res=[treenode]
    while res:
        print(res[0].data)
        tem=res.pop(0)
        if tem.lchild:
            res.append(tem.lchild)
        if tem.rchild:
            res.append(tem.rchild)


def inorder(root):     #中序遍历二叉树
    if root:
        inorder(root.lchild)
        print(root.data)
        inorder(root.rchild)

def preorder(treenode): #先序遍历
    if treenode:
        print(treenode.data)
        preorder(treenode.lchild)
        preorder(treenode.rchild)

def lasorder(treenode):     #后序遍历
    if treenode:
        lasorder(treenode.lchild)
        lasorder(treenode.rchild)
        print(treenode.data)

def deletenode(treenode,key):
    if search(tree1,key) is None:
        print('无可删除节点')
        return None
    node=search(tree1,key)
    if node.is_leaf():  #如果此节点为叶子节点 切断与双亲的联系
        print('被删除结点为叶子结点')
        if node.is_lchild():
            node.parent.lchild=None     #左子树
            node=None
            print('叶子结点删除成功')
            return True
        else:
            node.parent.rchild=None     #右子树
            node=None
            print('叶子结点删除成功')
            return True

    if node.has_any_child():    #如果该节点有一个以上的节点
        print('被删除结点有子树')
        if node.has_lchild() and not node.has_rchild():     #如果含有左子树，那么用左子树上的节点代替被删除的节点
            print('被删除结点只有左子树')
            node.parent.lchild=node.lchild
        elif node.has_rchild() and not node.has_lchild():
            print('被删除结点只有右子树')
            node.parent.rchild=node.rchild
        elif node.has_both_child(): #如果该节点拥有左右子树，那么用中序前驱或者后继节点来代替 左子树最大 右子树最小
            print('被删除结点有左右子树')
            if not node.lchild.has_any_child() and  node.rchild.has_any_child(): #如果被删除结点俩个左子树中为个叶子结点
                node.data=node.lchild.data      #左子树代替
                node.lchild=None
                return
            if node.lchild.has_any_child() and  not node.rchild.has_any_child(): #如果被删除结点俩个左子树中为个叶子结点
                node.data=node.rchild.data      #右子树
                node.rchild=None
                return
            if node.lchild.has_lchild():
                while node.lchild.has_lchild():
                    new_node=node.lchild.lchild
                    node=new_node.data
                    new_node.parent=None
                    print('删除成功2')
                    return
            if  node.rchild.has_rchild():
                while node.rchild.has_rchild():
                    new_node=node.rchild.rchild
                    node=new_node.data
                    new_node.parent=None
                    print('删除成功3')
                    return

tree1=TreeNode()
tree2=TreeNode()
tree3=TreeNode()
tree4=TreeNode()
tree5=TreeNode()
tree6=TreeNode()
tree7=TreeNode()
tree8=TreeNode()
tree9=TreeNode()
tree10=TreeNode()
tree11=TreeNode()
tree12=TreeNode()



#需要自己规定二叉树的节点大小 需符合规则
tree1.data,tree1.parent,tree1.lchild,tree1.rchild=(6,None,tree2,tree3)  #根节点
tree2.data,tree2.parent,tree2.lchild,tree2.rchild=(3,tree1,tree10,None)
tree3.data,tree3.parent,tree3.lchild,tree3.rchild=(14,tree1,tree4,tree5)
tree4.data,tree4.parent,tree4.lchild,tree4.rchild=(10,tree3,tree6,tree7)
tree5.data,tree5.parent,tree5.lchild,tree5.rchild=(16,tree3,None,None)
tree6.data,tree6.parent,tree6.lchild,tree6.rchild=(9,tree4,None,None)
tree7.data,tree7.parent,tree7.lchild,tree7.rchild=(13,tree4,tree8,None)
tree8.data,tree8.parent,tree8.lchild,tree8.rchild=(11,tree7,None,tree9)
tree9.data,tree9.parent,tree9.lchild,tree9.rchild=(12,tree7,None,None)
tree10.data,tree10.parent,tree10.lchild,tree10.rchild=(2,tree2,tree11,None)
tree11.data,tree11.parent,tree11.lchild,tree11.rchild=(1,tree10,tree12,None)
tree12.data,tree12.parent,tree12.lchild,tree12.rchild=(0,tree11,None,None)




# print(search(tree1,5))    #搜索二叉树

# insert(tree1,6)     #插入后查找该节点
# print(search(tree1,6))

#深度优先
# depth_first_show(tree1)
#广度优先
# width_first_show(tree1)

# inorder(tree1)    #中序
# preorder(tree1)   #先序
# lasorder(tree1)   #后序

# deletenode(tree1,6)
# inorder(tree1)