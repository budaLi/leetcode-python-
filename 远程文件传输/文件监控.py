# @Time    : 2020/3/15 15:37
# @Author  : Libuda
# @FileName: 文件监控.py
# @Software: PyCharm

import time
import paramiko

from 远程文件传输.register import register

# 时间间隔
time_sleep = 30


transport = paramiko.Transport(("103.96.148.50", 22000))  # 获取Transport实例
transport.connect(username="root", password="trfqw8ce")  # 建立连接

# 创建sftp对象，SFTPClient是定义怎么传输文件、怎么交互文件
sftp = paramiko.SFTPClient.from_transport(transport)

# # 将本地 文件上传至服务器 文件上传并重命名为test.py
# sftp.put("D:\PycharmProjects\leetcode-python-\远程文件传输\main.py", "test.py")


while 1:

    with open("phone.txt") as f:
        lines = len(f.readlines())  # 存储原来手机号的个数

    sftp.get("/home/fddsgzh/phone.txt", "phone.txt")
    with open("phone.txt") as f:  # 新文件
        data = f.readlines()

    for i in range(lines, len(data)):  # 获取新手机号的索引
        phone = data[i]
        print("获取手机号：{},等待开卡中。。".format(phone))
        # 去开卡
        res, lenght = register(phone)
        with open("res.txt", "a") as f:
            s = "手机号:{},开卡结果:{},剩余链接数:{}".format(phone, res, lenght)
            print(s)
            f.write(s + "\n")

    time.sleep(time_sleep)




# 关闭连接
# transport.close()
