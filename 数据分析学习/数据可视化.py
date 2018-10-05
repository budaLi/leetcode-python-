#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/10/5
import sys
reload(sys)
sys.setdefaultencoding('gbk')
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
#可选类型 font.sans-serif     : Bitstream Vera Sans, Lucida Grande, Verdana, Geneva, Lucid, Arial, Helvetica, Avant Garde, sans-serif
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
import pymysql
import pandas
import numpy
import matplotlib.pyplot as plt
conn=pymysql.connect(host='127.0.0.1',user='root',passwd='123',db='movie',charset='utf8')
sql='select * from lagou_job'
date=pandas.read_sql(sql,conn)

# date['work_years_min'].value_counts().plot(kind='barh',rot=45)  #rot表示坐标显示数据的倾斜程度
# plt.show()
#
# date['work_years_max'].value_counts().plot(kind='barh',rot=45)
# plt.show()

# date['degree_need'].value_counts().plot(kind='barh',rot=0)
# plt.show()

#词云的绘制
from wordcloud import WordCloud
import jieba
#从title列取出所有职位再用jieba进行分词
final=''
stopwords=['python','Python','PYTHON','工程师']
for n in range(date.shape[0]):   #表示每一行数据
    seg_list=list(jieba.cut(date['title'][n]))
    for seg in seg_list:
        if seg not in stopwords:
            final+=seg+' '
#词云绘制
#此处的字体路径可在自己的电脑中搜fonts可找到 指定路径即可
my_word_cloud=WordCloud(background_color='white',max_words=40,font_path=r"C:\Windows\Fonts\simsun.ttc",
                        min_font_size=5,max_font_size=50,width=400)
my_word_cloud.generate(final)
plt.imshow(my_word_cloud)
plt.axis('off')
plt.show()


#生成饼图
date['company_develop_state'].value_counts().plot(kind='pie',autopct='%1.2f%%')
plt.axis('equal')   #保证饼图是圆的
plt.show()