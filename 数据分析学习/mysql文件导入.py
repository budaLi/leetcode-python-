#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/10/1
import pymysql
import pandas
import numpy


def convert(values):
    if len(values)==0: return 0
    try:
        return float(values)
    except Exception as e:
        print(e)
conn=pymysql.connect(host='127.0.0.1',user='root',passwd='123',db='movie')
sql='select score from cartoon_movie'
k=pandas.read_sql(sql,conn)
print(len(k.values))   #数据个数
print(len(k.values[1])) #字段数
k['score']=k['score'].apply(convert)    #此处可以用函数对数据进行转换
# print(k.dtypes) #返回数据类型
print(k)

#离差标准化 将大数据转换为小数据
#又叫最大最小标准化
#消除单位影响以及变异大小因素的影响
# data1=(k-k.min())/(k.max()-k.min())
# print(data1)


#标准差标准化 消除单位影响以及变量自身变异影响
#零-均值标准化
#会得到平均数是0  标准差是1 的数据
#mean 平均值 std 标准差
# data2=(k-k.mean())/k.std()
# print(data2)


#小数定标规范化 将数据增大或减小
# tem=numpy.ceil(numpy.log10(k.abs().max()))
# data3=k/(10**tem)
# print(data3)