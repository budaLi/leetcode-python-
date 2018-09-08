#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/16
#简单选择排序的思想就是每次从要排序的数据中选取最大值或者最小值与第一个值交换，
#第二轮则变为从第二个数据开始到最后重新开始排序
#时间复杂度 n^^2
def select_sort(lis):       #正向排序
    count=len(lis)
    for i in range(1,count):    #n-1轮
        index=lis.index(min(lis[i-1:]))
        lis[i-1],lis[index]=lis[index],lis[i-1]
        print('第%s轮结果%s'%(i,lis))
    return lis


res=select_sort([7,5,4,8,9,2,10,1])
print(res)