#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/9/21
def reverseVowels(s):
    """
    :type s: str
    :rtype: str
    """
    tem1=[]
    pre=['a','e','i','o','u','A','E','I','O','U']
    for i in range(len(s)):
        if s[i] in pre:
            tem1.append(i)
    s=list(s)
    print(tem1)
    for i in range(len(tem1)/2):
        print(s[tem1[-len(tem1)+i]],s[tem1[-i-1]])
        s[tem1[-len(tem1)+i]],s[tem1[-i-1]]=s[tem1[-i-1]],s[tem1[-len(tem1)+i]]
    return ''.join(s)

#'hello'
#'ai'
#"Marge, let's \"went.\" I await news telegram."
s=r"hello"

res=reverseVowels(s)
print(res)


