# @Time    : 2019/12/10 12:56
# @Author  : Libuda
# @FileName: mytest.py
# @Software: PyCharm

# coding:utf-8
# Filename:hello_world.py
# 验证服务器，并且收到的所有消息都回复'Hello World!'

import werobot

robot = werobot.WeRoBot(token='asdfghgfdsaasdfggfdsasdf')


# @robot.handler 处理所有消息
@robot.handler
def hello(message):
    return '我是你爸爸!'


# 让服务器监听在 0.0.0.0:80
robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
robot.run()
