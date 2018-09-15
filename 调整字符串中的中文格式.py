#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/9/15
# import os
# print(os.listdir('.'))  #可以返回当前目录下的所有文件
#
#
# #得到当前目录下所有以Py结尾的文件
# print([name for name in os.listdir('.') if name.endswith('py')])
# print([name for name in os.listdir('.') if name.startswith('py')])

#调整字符产中的文本格式
tem='ahsjdbkasjdasld;2015-05-21ajskjl;'
import re
ss=re.match('.*?(\d{4}-\d{2}-\d{2})',tem)
if ss:
    ss=ss.group(1)
    ss=ss.replace('-','/')
print(ss)