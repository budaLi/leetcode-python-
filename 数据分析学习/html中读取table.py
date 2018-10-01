#-*- coding:utf8 -*-
#author : Lenovo
#date: 2018/10/1
import pandas

ss=pandas.read_html('http://www.xicidaili.com/')
print(ss)

#报错 urllib2.HTTPError: HTTP Error 503: Service Temporarily Unavailable
#可能是没有请求头被禁了