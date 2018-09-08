#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/16
#冒泡排序指的是对一组数据中的相邻两个数依次进行比较，共比较n-1轮，每次选出最大值或者最小值放在
#这组数据的开头或者末尾
def bubble_sort(lists):
    count=len(lists)
    for i in range(1,count):  #轮次 从第一轮到n轮
        print('第%s轮：'%i)
        for j in range(0,count-i):
            if lists[j]>lists[j+1]:
                lists[j],lists[j+1]=lists[j+1],lists[j]
        print('交换结果:%s'%lists)
    return lists

res=bubble_sort([1,3,4,5,2,10,6,0,7,9,8])
print('answer is %s'%res)