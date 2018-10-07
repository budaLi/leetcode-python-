#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/10/7
def reverseOnlyLetters(S):
    """
    :type S: str
    :rtype: str
    """
    S=list(S)
    left=0
    right=len(S)-1
    while left<right:
        while left<right and not (65<=ord(S[left])<=90 or 97<=ord(S[left])<=122):
            left+=1
        while left<right and not (65<=ord(S[right])<=90 or 97<=ord(S[right])<=122):
            right-=1
        S[left],S[right]=S[right],S[left]
        left+=1
        right-=1
        print(S)
    return ''.join(S)

s="a-bC-dEf-ghIj"
res=reverseOnlyLetters(s)
print(s)
print(res)
print(ord('='))