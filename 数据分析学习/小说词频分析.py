#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/10/2
#随便找了份爬取的小说，，好像涉黄了。。

import jieba
import jieba.analyse

with open('xiaoshuo.txt','r') as f:
    data=f.read()
    res=jieba.analyse.extract_tags(data,20)
    for item in res:
        print(item)