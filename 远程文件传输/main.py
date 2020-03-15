# @Time    : 2020/3/15 15:37
# @Author  : Libuda
# @FileName: main.py
# @Software: PyCharm
# import paramiko
#
# ##1.创建一个ssh对象
# client = paramiko.SSHClient()
#
# #2.解决问题:如果之前没有，连接过的ip，会出现选择yes或者no的操作，
# ##自动选择yes
# client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#
# #3.连接服务器
# client.connect(hostname='103.96.148.50',
#                port=22000,
#                username='root',
#                password='trfqw8ce')
# #4.执行操作
# stdin,stdout, stderr = client.exec_command('hostname')
#
# #5.获取命令执行的结果
# result=stdout.read().decode('utf-8')
# print(result)
#
# #6.关闭连接
# client.close()


import paramiko

transport = paramiko.Transport(("103.96.148.50", 22000))  # 获取Transport实例
transport.connect(username="root", password="trfqw8ce")  # 建立连接

# 创建sftp对象，SFTPClient是定义怎么传输文件、怎么交互文件
sftp = paramiko.SFTPClient.from_transport(transport)

# 将本地 文件上传至服务器 文件上传并重命名为test.py
sftp.put("D:\PycharmProjects\leetcode-python-\远程文件传输\main.py", "test.py")

# 将服务器test.py 下载到本地 文件下载并重命名为aaa.py
sftp.get("test.py", "aaa.py")

# 关闭连接
transport.close()
