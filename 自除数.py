#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/27
def selfDividingNumbers(left, right):
    """
    :type left: int
    :type right: int
    :rtype: List[int]
    """
    res=[]
    for one in range(left,right+1):
        tem=one
        if one/10!=0:
            res.append(one)
            for i in range(len(str(one))):
                n=one%10
                if n==0:
                    res.pop()
                    break
                elif tem%n!=0:
                    res.pop()
                    break
                else:
                    one=one/10
        else:
            res.append(one)

    return res


res=selfDividingNumbers(1,22)
print(res)