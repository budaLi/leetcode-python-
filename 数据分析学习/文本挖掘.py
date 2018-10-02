#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/10/2
#中文分词
import jieba
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#分词模式 全模式 精准模式 搜索引擎模式
sentence=u'我喜欢中国共产党'

#全模式
# res1=jieba.cut(sentence,cut_all=True)
# print('全模式：')
# for item in res1:
#     print(item)
#
# print('\n')
# #精准模式  默认为精准模式
# res2=jieba.cut(sentence,cut_all=False)
# print('精准模式:')
# for item in res2:
#     print(item)
#
# print('\n')
#
# #搜索引擎模式 倒排索引
# res3=jieba.cut_for_search(sentence)
# print('搜索引擎模式：')
# for item in res3:
#     print(item)

#词性标注
import jieba.posseg
#a  形容词
#c  连词
#d  副词
#e  叹词
#f 方位词
#i 成语
#m 数词
#n 名词
#nr 人名
#ns 地名
#nt 机构团体
#nz 其他专有名词
#p 介词
#r 代词
#t 时间
#u 助词
#v 动词
#vn 动名词
#w 标点符号
#un 未知词
# res4=jieba.posseg.cut(sentence)
#flag 词性
#word 词语
# for item in res4:
#     print(item.word+':'+item.flag)

#自定义词典加载 指定文件路径即可 需对应格式
#不是持久化存储
# jieba.load_userdict('')

#更改词频
# word='利布达和狗狗'
# res5=jieba.posseg.cut(word)
# for item in res5:
#     print(item.word+'  '+item.flag)
# jieba.add_word('利布达')

#更改后
# res6=jieba.posseg.cut(word)
# for item in res6:
#     print(item.word+'  '+item.flag)


#提取文本中的关键词
#分析文本中常见的词语
# import jieba.analyse
# res7=jieba.analyse.extract_tags('我爱你而么么么哒',3)   #参数 提取几个关键词
# print(res7[0])

#返回词语的位置
res8=jieba.tokenize(sentence)
for item in res8:
    print(item[0]+' '+str(item[1])+' '+str(item[2]))