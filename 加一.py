#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/8
def plusOne(digits):
    if len(digits)==0:
        return [1]
    flag=0
    res=list(reversed(digits))  #列表反转
    for i in range(len(res)):
        if i==0:
            tem=(res[i]+1)%10
            flag=int((res[i]+1)/10)
            res[i]=tem
            continue
        tem=(res[i]+flag)%10
        flag=int((res[i]+flag)/10)
        res[i]=tem
    if flag==1:
        res.append(1)
    return list(reversed(res))

res=plusOne([9,9])
print(res)