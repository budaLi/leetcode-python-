#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/10/8
def intersection(nums1, nums2):
    """
    :type nums1: List[int]
    :type nums2: List[int]
    :rtype: List[int]
    """
    #选择nums1作为较小的数组
    if len(nums1)>len(nums2):
       nums1,nums2=nums2,nums1
    res=[]
    nums2=set(nums2)
    for one in list(set(nums1)):    #两个都去重速度更快
        if one in nums2:
            res.append(one)

    return res


res=intersection(nums1 = [4,9,5], nums2 = [9,4,9,8,4])
print(res)
