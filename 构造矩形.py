#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/10/2
def constructRectangle(area):
    """
    :type area: int
    :rtype: List[int]
    """
    import math
    l=int(math.sqrt(area))
    r=int(math.sqrt(area))
    while l*r!= area:
        l-=1
        r=area/l
    if r>l:
        l,r=r,l
    return [l,r]

res=constructRectangle(10)
print(res)