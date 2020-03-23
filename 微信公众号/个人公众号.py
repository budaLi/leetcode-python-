# @Time    : 2020/3/19 17:22
# @Author  : Libuda
# @FileName: 个人公众号.py
# @Software: PyCharm
# coding: utf-8
import re
import requests
import csv
import werobot

robot = werobot.WeRoBot(token='asdfghgfdsaasdfggfdsasdf')


# 被关注自动回复
# @robot.subscribe
def subscribe(message):
    return "嘟嘟最可爱"


# 接受信息自动回复
# @robot.handler
def search(keyword):
    return "嘟嘟最可爱 啦啦啦啦"


if __name__ == '__main__':
    robot.config['HOST'] = '127.0.0.1'
    robot.config['PORT'] = 80
    robot.run()
