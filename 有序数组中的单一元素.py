#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/1


def Binary_search(lis):
    low=0
    high=len(lis)-1
    if len(lis)%2==0:
        return None
    while(low<=high):
        mid=int((low+high)/2)
        if mid==low==high:
            return lis[mid]
        if lis[mid]==lis[mid-1] and mid%2==1:  #如果mid==mid-1且mid是奇数 说明单一元素在之后
            low=mid+1
        elif lis[mid]==lis[mid-1] and mid%2==0:
            high=mid-1
        elif lis[mid]==lis[mid+1] and mid%2==1:
            high=mid-1
        elif lis[mid]==lis[mid+1] and mid%2==0:
            low=mid
        else:
            return lis[mid]
A=[1]
res=Binary_search(A)
print(res)
