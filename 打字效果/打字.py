#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/9/16
import sys,time

with open("text", 'r', encoding='utf-8') as f:
    for line in f.readlines():  # 循环读取行
        for i in line: #循环读取文字
            sys.stdout.write(i) #标准输出
            sys.stdout.flush() #刷新
            time.sleep(0.01) #输出时间控制