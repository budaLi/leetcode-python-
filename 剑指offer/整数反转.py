#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/10/23
def trans(number):
    flag=''
    if number<0:
        flag='-'
    number=list(str(number))[::-1][:-1] if flag=='-' else list(str(number))[::-1]
    return int(flag+''.join(number))

res=trans(-321)
print(res)