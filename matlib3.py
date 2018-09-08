#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/8/26

import matplotlib.pyplot as plt
import numpy as np
# plt.rcParams['font.sans-serif']=['SimHei']
# plt.rcParams['axes.unicode_minus']=False
# import math
# x=np.linspace(-10,10,1000) #将区间等分为多少分
# y=np.cos(x)
# z=np.sin(x)
# plt.xlabel(u'区间')
# plt.ylabel(u'值')
# plt.plot(x,y,linestyle='-.',color='red',marker='*')
# plt.plot(x,z,linestyle='-.',color='green',marker='.')
# plt.show()  #



x=np.arange(10)
# y1=[10,20,30,40,50,60,70,80,90,100]
# y2=map(lambda x:x-3,y1)
# print(y2)
# plt.bar(left=x,width=0.3,color='red',height=y1)
# plt.bar(left=x+0.3,width=0.3,color='blue',height=y2)
# plt.show()

y1=[10,20,30,40,50,60,70,80,90,100]
y2=map(lambda x:x-3,y1)
plt.bar(left=x,width=0.3,color='red',height=y1)
plt.bar(left=x,width=0.3,color='blue',height=y2,bottom=y1)
plt.show()