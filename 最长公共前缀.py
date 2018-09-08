#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/5
def longestCommonPrefix(strs):
        res=''
        strs.sort(key=lambda x:len(x))
        if len(strs)==0:
            return res
        short_str=strs[0]
        if len(strs)==0:
            return res
        if len(strs)==1:
            return short_str
        for i in range(len(short_str)):
            for one_str in strs:
                if one_str==short_str:
                    res=short_str
                if one_str[i]!=short_str[i]:
                    return short_str[:i]
        return res
res=longestCommonPrefix(["a","b"])
print(res)