#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/9/20
def rotateString(A, B):
    """
    :type A: str
    :type B: str
    :rtype: bool
    """
    A=list(A)
    B=list(B)
    if len(set(A))!=len(set(B)): return False
    if A=="": return True
    for i in range(len(A)):
        A.append(A.pop(0))
        if A==B:
            return True
    return False

res=rotateString("",
"")
print(res)