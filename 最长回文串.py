#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/3
# 给定一个包含大写字母和小写字母的字符串，找到通过这些字母构造成的最长的回文串。
#
# 在构造过程中，请注意区分大小写。比如 "Aa" 不能当做一个回文字符串。
#
# 注意:
# 假设字符串的长度不会超过 1010。
#
# 示例 1:
#
# 输入:
# "abccccdd"
#
# 输出:
# 7
#
# 解释:


def longest(s):
    d={}
    tag=0
    res=0
    # for i  in range(len(s)):
    #     if s[i] not in d:
    #        d[s[i]]=s.count(s[i])
    for each in s:          #比上面好
        if each not in d:
            d[each]=s.count(each)
    print(d)
    for values in d.values():
        if values%2==0:
            res+=values
        elif values%2==1 and tag==0:
            res+=values
            tag=1
        elif values%2==1 and tag==1:
            res+=values-1
    return res


res=longest("bananas")
print(res)
#我们知道回文串是从中心对称的，那么这个回文串至少包含所有出现偶数次的元素，特殊情况当元素出现奇数个且大于一的情况时可以将其中的偶数个放入