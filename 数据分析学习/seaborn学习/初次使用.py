#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/10/5
import sys
reload(sys)
sys.setdefaultencoding('gbk')
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
def sinplot(flip=1):
    x=np.linspace(0,14,100)
    for i in range(1,7):
        plt.plot(x,np.sin(x+i**0.5)*(7-i)*flip)
    plt.show()

# sns.set()
# sinplot(2)


#seaborn中有五种主题风格

sns.set_style('dark')   #没有线
sns.set_style('white')  #背景白色
sns.set_style('ticks')  #x，y轴加上线段