#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/9/20
def rotatedDigits(N):
    """
    :type N: int
    :rtype: int
    """
    #数字中 2 5 6 9且没有 3 4 7即为好数
    import re
    count=0
    mat=re.compile('2|5|6|9')
    err=re.compile('3|4|7')
    for i in range(1,N+1):
        res=re.findall(mat,str(i))
        if res:
            tem=re.findall(err,str(i))
            if tem==[]:
                count+=1
    return count

res=rotatedDigits(857)
print(res)

