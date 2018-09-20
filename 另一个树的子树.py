#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/9/20

#时间很长 但是通过了
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution(object):
    def isSubtree(self, s, t):
        """
        :type s: TreeNode
        :type t: TreeNode
        :rtype: bool
        """
        def judge(s,t):
            tem1=[s]
            tem2=[t]
            flag=False
            while len(tem1)==len(tem2):
                if len(tem1)==0: break  #此处是两者都为空了
                elif tem1[0] and tem2[0]:
                    print(tem1[0].val,tem2[0].val)
                    if tem1[0].val == tem2[0].val:
                        flag=True
                        one=tem1.pop(0)
                        if one.left:
                            tem1.append(one.left)
                        if one.right:
                            tem1.append(one.right)
                        two=tem2.pop(0)
                        if two.left:
                            tem2.append(two.left)
                        if two.right:
                            tem2.append(two.right)
                    else:
                        flag=False
                        break
                #此处注意两者长度不一样也退出
                elif (tem1[0] and not tem2[0]) or (tem2[0] and not tem1[0]):
                    flag=False
                    break
            if len(tem1)!=len(tem2): return False
            return flag
        flag=False
        tem=[s]
        while tem:
            if tem[0].val==t.val:
                flag=judge(tem[0],t)
                if flag==True: return True
            one=tem.pop(0)
            if one.left:
                tem.append(one.left)
            if one.right:
                tem.append(one.right)
        return False


node1=TreeNode(3)
node2=TreeNode(4)
node3=TreeNode(5)
node4=TreeNode(1)
node5=TreeNode(2)
# node6=TreeNode(0)
node1.left=node2
node1.right=node3
node2.left=node4
node2.right=node5
# node4.left=node6

node7=TreeNode(4)
node8=TreeNode(1)
node9=TreeNode(2)

node7.left=node8
node7.right=node9


S=Solution()
res=S.isSubtree(node1,node7)
print(res)