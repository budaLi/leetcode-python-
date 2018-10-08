#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/10/8
def intersect(nums1, nums2):
    """
    :type nums1: List[int]
    :type nums2: List[int]
    :rtype: List[int]
    """
    dic1={}
    for one in nums1:
        if one not in dic1:
            dic1[one]=1
        else:
            dic1[one]+=1
    dic2={}
    for one in nums2:
        if one not in dic2:
            dic2[one]=1
        else:
            dic2[one]+=1
    res=[]
    for di in dic1:
        if di in dic2:
            res.extend(di for i in range(min(dic1[di],dic2[di])))
    return res

res=intersect(nums1 = [1,2,2,1], nums2 = [2,2])
print(res)