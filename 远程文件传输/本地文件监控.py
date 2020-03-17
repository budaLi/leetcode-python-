# @Time    : 2020/3/15 15:37
# @Author  : Libuda
# @FileName: 远程服务器文件监控.py
# @Software: PyCharm

import time

from 远程文件传输.register import register

# 时间间隔
time_sleep = 30

while 1:
    #  与phone.txt 对比 获取最新的手机号去开卡
    with open("old_phone.txt") as f:
        lines = len(f.readlines())  # 存储原来手机号的个数

    with open("phone.txt") as f:  # 新文件
        data = f.readlines()

    for i in range(lines, len(data)):  # 获取新手机号的索引
        phone = data[i].strip()
        print("获取手机号：{},等待开卡中。。".format(phone))
        # 去开卡
        res, lenght = register(phone)
        with open("res.txt", "a") as f:
            s = "手机号:{},开卡结果:{},剩余链接数:{}".format(str(phone), res, lenght)
            print(s)
            f.write(s + "\n")

        # a表示追加
        with open("old_phone.txt", 'a') as f:
            # 领卡后存入old_phone
            f.write(phone + "\n")

    time.sleep(time_sleep)
