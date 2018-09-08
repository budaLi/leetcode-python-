#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/6
def removeDuplicates(nums,key):
    length=len(nums)
    if length==0:
        return 0
    for j  in range(1,length):
        if nums[j]==key:
            nums[j]=nums[j+1]
    return nums  #由于数组下标是从0开始 长度应该+1

res=removeDuplicates([1,2,3,3,4,5,5],2)
print(res)
