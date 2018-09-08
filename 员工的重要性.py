#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/8/31
class Employee(object):
    def __init__(self, id, importance, subordinates):
        # It's the unique id of each node.
        # unique id of this employee
        self.id = id
        # the importance value of this employee
        self.importance = importance
        # the id of direct subordinates
        self.subordinates = subordinates


#思路
#首先应该找出该id对应的列表 加上值 再往后遍历它的下级
class Solution(object):
    def getImportance(self, employees, id):
        lis=[id]
        res=0
        while lis:
            print('ss',lis)
            for employ in employees:
                if lis:     #这里有可能存在这个id已经不存在下级了 再判断出错
                    if employ[0]==lis[0]:
                        print(res)
                        res+=employ[1]
                        print('res',res)
                        lis.extend(employ[2])
                        print('lis',lis)
                        lis.pop(0)
                        print('lis',lis)
        return res

S=Solution()
res=S.getImportance([[101,3,[]],[2,5,[101]]],
101
)
print(res)

ss=[1,2,3,4]
s2=[2222]
ss.extend(s2)
print(ss)