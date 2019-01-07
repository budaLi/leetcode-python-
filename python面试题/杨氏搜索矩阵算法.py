#-*-coding:utf8-*-
#author : Lenovo
#date: 2019/1/6


# 已知一个二维矩阵 其中元素每一行从左到右依次增加 每一列也是从上往下依次增加
# 这样的矩阵叫做杨氏矩阵

# 下面给出几种算法
# 原文地址   https://blog.csdn.net/sgbfblog/article/details/7745450
# 下面是我自己的总结



# -------------------------------------------------------------------------------------

# 1.二分查找

# 由于杨氏矩阵的特性 我们可以从第一行开始使用二分查找 到第n行 时间复杂度为 O(nlogn)

def Binarysearch(Matrix,target):
    def binarysearch(lis,tartget):  #能查到返回其对应索引 找不到则返回none
        start=0
        end=len(lis)-1
        while start<end:
            mid=(start+end)//2
            if lis[mid]==target:
                return mid
            elif lis[mid]<target:
                start=mid+1
            else:
                end=mid-1
        return None
    for i in range(len(Matrix)):
        if binarysearch(Matrix[i],target) is not None:
            return [i,binarysearch(Matrix[i],target)]
    return None


# tem=[[1,4,7,11,15],
#      [2,5,8,12,19],
#      [3,6,8,12,19],
#      [10,13,14,17,24],
#      [18,21,23,26,30]]
# print(tem)
# res=Binarysearch(tem,3)
# print(res)

# --------------------------------------------------------------------------------------

# step-wise 线性搜索算法
#从矩阵的右上角开始 依次与目标值比较 如果比目标值大 则直接去掉一列 如果小则去掉一行
# 时间复杂度为n  最坏情况为 2n

def StepWiseSearch(Matrix,target):
    l=len(Matrix)-1
    m=len(Matrix[0])-1

    start = 0
    while start<=l and start>=0 and m>=0:
        if Matrix[start][m]==target:
            return True
        elif Matrix[start][m]>target:   #如果比目标值大 则直接去掉一列
            m-=1
        else:
            start+=1
    return False

tem=[[1,4,7,11,15],
     [2,5,8,12,19],
     [3,6,8,12,19],
     [10,13,14,17,24],
     [18,21,23,26,30]]
print(tem)
res=StepWiseSearch(tem,222)
print(res)

# ----------------------------------------------------------------------------

#四分分解算法

#通过观察可以发现问题很容易通过分治法来解决 可以看到 矩阵中间的元素将矩阵分为四部分
# 这四部分也是排序好的  以上面矩阵为例  [[1,4,7,||，11,15],
#                                       [2,5,8, ||12,19],
#                                       [3,6,8, ||12,19],
#                                        ---------------
#                                      [10,13,14,||17,24],
#                                      [18,21,23,||26,30]]

#假如 我们要查找元素为17 可以看到第一部分中最大的元素 8<17 那么
# 我们就可以直接舍弃第一部分 在其余三个矩阵中查找
