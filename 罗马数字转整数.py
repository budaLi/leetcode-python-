#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/8/5
num={}
num['I']=1
num['V']=5
num['X']=10
num['L']=50
num['C']=100
num['D']=500
num['M']=1000
#例如 IVIII 当我们判断到I < V 则-I 再往后即可

def trans(x):
    res=0
    for i in range(len(x)):
        if i+1==len(x):
            res=res+num[x[i]]
            return res
        if num[x[i]]<num[x[i+1]]:    #如果左边比右边小则减去
            res=res-num[x[i]]
        else:
            res=res+num[x[i]]
    return res
re=trans('VV')
print(re)