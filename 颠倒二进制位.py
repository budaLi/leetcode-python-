#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/9/19
def reverseBits(n):
    n=bin(n)[2:]
    while len(n)<32:    #加0变32
        n='0'+n
    return int(''.join(list(reversed(n))),2)

res=reverseBits(43261596)
print(res)

