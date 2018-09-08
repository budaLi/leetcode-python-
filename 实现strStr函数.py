#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/6
# def strStr(haystack, needle):#效果不好 时间慢
#     if needle =='':
#         return 0
#     if (haystack == '' and needle!='') or len(haystack)<len(needle) :
#         return -1
#     for i in range(len(haystack)):
#         if needle[0] == haystack[i]:
#             if needle == haystack[i:len(needle)+i]:
#                 return i
#     return -1


def strStr(haystack, needle):   #时间最好
        len1=len(haystack)
        len2=len(needle)
        #我们设len1=m,len2=n,m>n,那么我们从0开始截取 也就是从[0,n-1] 到[m-n+1,m]一共截取了多少次
        #那么，我们知道当range里为负数的话不执行循环。直接返回-1即可
        #当len2为0时，直接第一次就和空相等。返回0
        for i in range(len1-len2+1):
            if haystack[i:i+len2]==needle:
                return i
        return -1
res=strStr("l", "")
print(res)
