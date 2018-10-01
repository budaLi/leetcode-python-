#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/10/1
#等宽离散化
#等频率离散化
#一维聚类离散化
import pymysql
import pandas
import numpy


#等宽离散化
conn=pymysql.connect(host='127.0.0.1',user='root',passwd='123',db='movie')
sql='select score from cartoon_movie'
k=pandas.read_sql(sql,conn)

data1=k
data1['score']=data1['score'].astype('float')
print(data1.values.dtype)

data2=data1.T   #对数据进行转置
#cut对数据进行划分 参数含义 第一个为数据 第二个为划分区域 可以为数字代表划分区域个数  列表形式为区间形式 第三个参数为划分的标签
ss=pandas.cut(data2.values[0],[1,8,10],labels=['1','2'])
print(ss)