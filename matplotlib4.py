#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/8/27
import matplotlib.pyplot as plt
import numpy as np
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题


labe=[u'我',u'最菜的嘟嘟']
plt.xlabel(u'个人能力分析图')
date=[100,0.1]
plt.axes(aspect=1)  #以圆显示
exolode=[0,0.0]
plt.pie(x=date,labels=labe,autopct='%.0f%%',explode=exolode,shadow=True,colors='c',labeldistance=0.8,startangle=50,radius=0.5,counterclock=0.0001)
plt.show()


