#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/10/9

#未完成
#垃圾思路 将所有可能出现的情况组合 此处利用itertools中的函数
#但p很大时肯定会超时 会产生很多种组合
def findAnagrams(s, p):
    """
    :type s: str
    :type p: str
    :rtype: List[int]
    """
    import itertools
    res={}

    #这个函数可以根据一个字符串产生所有可能的组合 但是是列表形式
    for one in itertools.permutations(p):
        res[''.join(one)]=1
    ans=[]
    for  i in range(len(s)-len(p)):
        if s[i] in p:
            if s[i:i+len(p)] in res:
                ans.append(i)
    return ans
res=findAnagrams("cbaebabacd","abc")
print(res)