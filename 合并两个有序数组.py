#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/9
def merge(nums1, m, nums2, n):
    if m==0 and n!=0:   #此处是将num1替换为nums2，但是直接nums1=nums2不行
        for i in range(n):
            nums1[i]=nums2[i]
            return nums1
    if m!=0 and n==0:
        nums1=nums1
        return nums1
    else:
        for i in range(n):
            nums1[m+i]=nums2[i]
        nums1.sort()
        return nums1
res=merge([1,2,3,0,0,0],3,[2,5,6],3)
print(res)