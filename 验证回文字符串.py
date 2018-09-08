#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/31
# def judge(s):
#     s1=s[::-1]
#     if s1==s:
#         return True
#     else:
#         return False
# def validPalindrome( s):
#     """
#     :type s: str
#     :rtype: bool
#     """
#     count=0
#     if judge(s):
#         return True
#     else:
#         s=list(s)
#         length=len(s)
#         if length%2==0:
#             s1=s[:length/2]
#             s2=list(reversed(s[-(length/2):]))
#         else:
#             s1=s[:length/2+1]
#             s2=list(reversed(s[-(length/2)-1:]))
#         for i in range(len(s1)):
#             if count<1:
#                 if s1[i]!=s2[i]:
#                     tem=s.pop(i)
#                     if judge(s): return True
#                     else:
#                         print(s)
#                         s.insert(i,tem)
#                         print(s)
#                         s.pop(-i-1)
#                         print(s)
#                         if judge(s): return True
#             else:
#                 return False

def validPalindrome(str1):
    """
    :type s: str
    :rtype: bool
    """
    str2=str1[::-1]
    if str1 == str2:
        return True
    for i in range(len(str1)//2):
        if str1[i] != str2[i]:
            if str1[i+1:len(str1)//2+1] == str2[i:len(str1)//2]:
                return True
            if str1[i:len(str1)//2] == str2[i+1:len(str1)//2+1]:
                return True
            return False
    return False
SS="ABBDA"
res=validPalindrome(SS)

print(res)