#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/10/2
#tf-idf 是一种用于信息检索和数据挖掘的常用加权技术

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#1。读取文档 进行分词 2，整理文档为指定格式 3 计算词频 4 词语过滤
#5 通过语料库建立词典 6.加载要对比的文档  7 通过doc2bow 将要对比的文档转化为稀疏向量
#8 对稀疏向量进行进一步处理 得到新语料库 9 将新语料库通过tf-idf 进行处理 得到td-idf 的值
#10 通过token2id 得到特征数  11 得到稀疏矩阵相似度 建立索引 得到相似度结果

from gensim import corpora #语料库
from gensim import models #模型
from gensim import similarities #相似度
import jieba

doc1='doc1.txt'
doc2='doc2.txt'

with open(doc1,'r') as f1:
    data1=f1.read()
with open(doc2,'r') as f:
    data2=f.read()

data1=data1.replace(' ','')
data2=data2.replace(' ','')

#分词
lis1=jieba.cut(data1)
lis2=jieba.cut(data2)


tem1=''
tem2=''
for item in lis1:
    print(item)
    tem1+=item.encode('utf8')
for item in lis2:
    tem2+=item.encode('utf8')

print(tem1)
# print(tem2)

# documents=[tem1,tem2]
# text=[[word for word in document.split()] for document in documents]
# print(text)
#整理为指定格式  '词语1 词语2 词语3'


