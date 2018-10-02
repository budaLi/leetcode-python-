#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/10/1
import pymysql
import pandas
import numpy
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

conn=pymysql.connect(host='127.0.0.1',user='root',passwd='123',db='movie',charset='utf8')
sql='select * from cartoon_movie'
k=pandas.read_sql(sql,conn)
k['movie_name']=k['movie_name'].astype('str')
print(k)
k.to_csv('C:\Users\Lenovo\Desktop\data.csv',index=False)