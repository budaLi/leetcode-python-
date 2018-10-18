#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/10/4
# from collections import OrderedDict   #垃圾
# def maxAreaOfIsland(grid):
#     """
#     :type grid: List[List[int]]
#     :rtype: int
#     """
#     if len(grid)==1: #变为一维的 求连续的1的个数
#         res=0
#         count=0
#         for i in range(len(grid[0])):
#             if grid[0][i]==1: count+=1
#             else: count=0
#             res=max(res,count)
#         return res
#     dic=OrderedDict()
#     for i in range(len(grid)):  #将1的值存起来
#         for j in range(len(grid[0])):
#             if grid[i][j]==1:
#                 dic[i,j]=1
#     def get_around_max(i,j):    #得到该位置四周的四个元素在字典
#         max_x=1
#         count=0
#         for one in [[i-1,j],[i+1,j],[i,j-1],[i,j+1]]:
#             if (one[0],one[1]) in dic:
#                 if dic[one[0],one[1]]>1 and dic[one[0],one[1]]>max_x:
#                     if max_x>dic[one[0],one[1]]:
#                         count+=1
#                     max_x=dic[one[0],one[1]]
#                 else:
#                     count+=1
#         return max_x+count
#     for one in dic:
#         dic[one]=get_around_max(one[0],one[1])
#
#     return dic

class Solution(object):
    def dfs(self, grid, x0, y0):
        s = 1
        n = len(grid)
        m = len(grid[0])

        grid[x0][y0] = 0
        dire = [[0,1],[0,-1],[1,0],[-1,0]]
        for i in range(0,4):
            x = x0 + dire[i][0]
            y = y0 + dire[i][1]
            if x>=0 and x<n and y>=0 and y<m and grid[x][y] == 1:
                s = s + self.dfs(grid, x, y)
        return s


    def maxAreaOfIsland(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """
        mx = 0
        n = len(grid)
        m = len(grid[0])
        for i in range(0, n):
            for j in range(0, m):
                if grid[i][j] == 1:
                    mx = max(mx, self.dfs(grid, i,j))
        return mx

S=Solution()
res=S.maxAreaOfIsland([[1,0,1,1],[1,0,1,1]])


print(res)