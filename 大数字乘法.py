#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/7/29
import datetime
class Solution():
    def __init__(self):
        pass
    def big_date_mul(self,num1,num2):
        start=datetime.datetime.now()
        import time
        tem=[]
        res=[]
        flag=0
        big=200
        for i in range(len(str(num1))):
            tem.append(str(num1)[i])
            res.append(0)
        tem=list(reversed(tem))
        for i in range(big-len(tem)):
            tem.append(0)
            res.append(0)
        for i in range(big):
            res[i]=(int(tem[i])*num2+flag)%10
            flag=int((int(tem[i])*num2+flag)/10)
        res=list(reversed(res))
        tem.clear()
        for i in range(len(res)):
            if res[i] != 0:
                tem.append(res[i])
        end=datetime.datetime.now()
        print('time',end-start)
        return str(tem)
s=Solution()
sa=s.big_date_mul(761465464654646111111111111146464623222,1212121212113121298765432345678765431111111111111111111111111112122138)
print(sa)

def mul(num1,num2):
    start=datetime.datetime.now()
    res=num1*num2
    end=datetime.datetime.now()
    print(res)
    print(end-start)
mul(761465464654646111111111111146464623222,1212121212113121298765432345678765431111111111111111111111111112122138)
