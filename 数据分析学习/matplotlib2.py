#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/8/26
import matplotlib.pyplot as plt
import numpy as np

# x=np.arange(1,100)  #生成数
# plt.plot([1,2,3],[2,3,4])
# plt.plot([3,4,5],[2,3,2])
# plt.grid(True)
# plt.grid(color='r',linestyle='-.')
# plt.show()



#散点图    #正相关 负相关 不相关
# x=[1,2,3,4,5,7,8,9,0]
# y=[3,4,4,5,7,9,0,0,100]

# x=np.random.randn(1000) #不相干
# y=np.random.randn(1000)

# x=np.arange(1,10) #正相关
# y=x*3-2
#
x=np.arange(1,10)   #负相关
y=-x*3-2

plt.scatter(x,y,s=500,edgecolors='r',marker='*',alpha=0.5,c='b')
plt.show()