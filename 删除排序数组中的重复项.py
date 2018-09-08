#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/6
#双指针法

def removeDuplicates(nums):
    i=0 #慢指针
    length=len(nums)
    for j  in range(1,length):
        if nums[i]!=nums[j]:
            i=i+1
            nums[i]=nums[j]
    return i+1  #由于数组下标是从0开始 长度应该+1

res=removeDuplicates([1,2,3,3,4,5,5])
print(res)
