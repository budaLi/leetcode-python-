#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/9/20
def compress(chars):
    """
    :type chars: List[str]
    :rtype: int
    """
    if len(set(chars))==len(chars): return len(chars)
    tem=list(set(chars))
    print(tem)
    for i in range(0,len(tem)):
        for j in range(0,len(chars),2):
            if chars.count(tem[i])>1:
                chars[j],chars[j+1]=tem[i],str(chars.count(tem[i]))
    print(chars)
    return len(set(chars))*2


res=compress(["a","a","b","b","c","c","c"])
print(res)