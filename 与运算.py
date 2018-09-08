#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/3


import datetime
n=0
max_compare=1000000
date=1000000000000000000001
#与运算判断是否是奇数
start1=datetime.datetime.now()
while n<max_compare:
    if date&1:
        n+=1
end1=datetime.datetime.now()
print('time1:',end1-start1)



start2=datetime.datetime.now()
while n<max_compare:
    if date%2==1:
        n+=1
end2=datetime.datetime.now()

print('time2:',end2-start2)