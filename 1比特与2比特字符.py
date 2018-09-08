#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/20
def isOneBitCharacter(bits):
    """
    :type bits: List[int]
    :rtype: bool
    """
    while len(bits)>2:
        if bits[0]==1:
            bits=bits[2:]
        else:
            bits=bits[1:]
    if bits==[1,0]:
        return False
    elif bits==[0,0] or bits==[0]:
        return True


res=isOneBitCharacter([1,1,1,1,1,0,0,0,0,1,1,1,1,0])
print(res)