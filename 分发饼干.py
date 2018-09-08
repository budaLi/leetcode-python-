#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/23
# k = raw_input()           #百度
# n = int(raw_input())
# length = len(k)
# dp = [0] * n
# if k[0] == 'X':
#     for d in range(10):
#         _ = d % n
#         dp[_] += 1
# else:
#     dp[int(k[0]) % n] = 1
#
# for i in range(1, length):
#     new_dp = [0] * n
#     for j in range(n):
#         if dp[j]:
#             if k[i] == 'X':
#                 for d in range(10):
#                     new_j = (j*10+d) % n
#                     new_dp[new_j] += dp[j]
#             else:
#                 new_j = (j*10+int(k[i])) % n
#                 new_dp[new_j] += dp[j]
#     dp = new_dp
#
# print(dp[0])
# dp = [0] * 10
# print(dp)



def findContentChildren(g, s):
    """
    :type g: List[int]
    :type s: List[int]
    :rtype: int
    """
    count=0
    g=sorted(g)
    s=sorted(s)
    while len(g) and len(s):
        if s[0]<g[0]:
            s.pop(0)
        else:
            s.pop(0)
            g.pop(0)
            count+=1
    return count
res=findContentChildren([10,9,8,7],
[5,6,7,8])
print(res)


ss=[1,6,4,5]
sss=[1,4,7,2]
print(sorted(ss))


print(sorted(sss))