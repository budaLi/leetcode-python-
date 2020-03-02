# @Time    : 2020/2/28 13:30
# @Author  : Libuda
# @FileName: main.py
# @Software: PyCharm
# -*- coding: utf-8 -*-

import poplib, email, telnetlib
import datetime, time, sys, traceback
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import imaplib


def logger(msg):
    """
    日志信息
    """
    now = time.ctime()
    print("[%s] %s" % (now, msg))



class down_email():

    def __init__(self, user, password, eamil_server):
        # 输入邮件地址, 口令和POP3服务器地址:
        self.user = user
        # 此处密码是授权码,用于登录第三方邮件客户端
        self.password = password
        self.pop3_server = eamil_server
        self.count = 0
        self.totle_set = None  # 邮件去重
        self.connect_server()
        self.server.user(self.user)
        self.server.pass_(self.password)

    def connect_server(self):
        try:
            telnetlib.Telnet(self.pop3_server, 995)
            self.server = poplib.POP3_SSL(self.pop3_server, 995, timeout=10)
        except:
            self.server = poplib.POP3(self.pop3_server, 110, timeout=10)


    # 获得msg的编码
    def guess_charset(self, msg):
        charset = msg.get_charset()
        if charset is None:
            content_type = msg.get('Content-Type', '').lower()
            pos = content_type.find('charset=')
            if pos >= 0:
                charset = content_type[pos + 8:].strip()
        return charset

    # 获取邮件内容
    def get_content(self, msg):
        content = ''
        content_type = msg.get_content_type()
        # print('content_type:',content_type)
        if content_type == 'text/plain':  # or content_type == 'text/html'
            content = msg.get_payload(decode=True)
            charset = self.guess_charset(msg)
            if charset:
                content = content.decode(charset)
        return content

    # 字符编码转换
    # @staticmethod
    def decode_str(self, str_in):
        value, charset = decode_header(str_in)[0]
        if charset:
            value = value.decode(charset)
        return value

    # 解析邮件,获取内容
    def get_att(self, msg_in):
        result = []
        for part in msg_in.walk():
            # 是文本内容
            content = self.get_content(part)
            if content:
                result.append(content)
        return ",".join(result)

    def run_ing(self, users, second):

        # 打印POP3服务器的欢迎文字:
        # print("身份验证成功，下面为测试输出：{}".format(self.server.getwelcome().decode('utf-8')))
        # 身份认证:

        # 返回邮件数量和占用空间:
        logger('邮件总数: %s. 大小: %s' % self.server.stat())

        # list()返回所有邮件的编号:
        resp, mails, octets = self.server.list()
        # 可以查看返回的列表类似[b'1 82923', b'2 2184', ...]

        if self.count == 0:
            # 如果是第一次
            index = []
            self.count = len(mails)
        else:
            index = [i for i in range(self.count + 1, len(mails) + 1)]
            self.count = len(mails)

        for i in index:  # 倒序遍历邮件
            # for i in range(1, index + 1):# 顺序遍历邮件
            resp, lines, octets = self.server.retr(i)
            # lines存储了邮件的原始文本的每一行,
            # 邮件的原始文本:
            try:
                msg_content = b''.join(lines).decode('utf-8')
                # 解析邮件:
                msg = Parser().parsestr(msg_content)
            except Exception as e:
                print(b''.join(lines))
                pass



            # 方法2：from or Form均可
            From = parseaddr(msg.get('from'))[1]
            To = parseaddr(msg.get('To'))[1]
            Cc = parseaddr(msg.get_all('Cc'))[1]  # 抄送人
            Subject = self.decode_str(msg.get('Subject'))
            date1 = time.strptime(msg.get("Date")[0:24], '%a, %d %b %Y %H:%M:%S')


            # 邮件时间格式转换
            date2 = time.strftime("%Y-%m-%d %H:%M:%S", date1)

            if From in users:
                # print(date2,start_time)
                print("\n")
                print('发件人:%s,收件人:%s,抄送人:%s,主题:%s，发件时间：%s' % (From, To, Cc, Subject, date2))
                content = self.get_att(msg)
                print("邮件正文:{} \n".format(content.replace("&nbsp;", "")))
        # 可以根据邮件索引号直接从服务器删除邮件:
        # self.server.dele(7)
        self.server.noop()


def main():
    # 收件人邮箱及密码
    user_tem = "qihuoxinhao{}@163.com"
    password = 'A1234567'

    # 读取收件人
    user_lis = []
    with open("user") as f:
        datas = f.readlines()
        for one in datas:
            user_lis.append(one.strip())
    # 指定发件人
    users = ['WebStockWh8@wenhua.com.cn', '3405987953@qq.com', '1364826576@qq.com', '1410000000@qq.com']
    # 刷新时间间隔
    time_s = 1

    eamil_server = 'pop.163.com'
    user = user_lis.pop(0)
    user_lis.append(user)
    email_class = down_email(user=user, password=password, eamil_server=eamil_server)

    while 1:
        try:
            print("当前使用用户：{}".format(user))
            time.sleep(time_s)
            email_class.run_ing(users, time_s)
        except Exception as e:
            print(e)
            print("出现异常 切换用户中")
            user = user_lis.pop(0)
            user_lis.append(user)
            email_class = down_email(user=user, password=password, eamil_server=eamil_server)


def test():
    # 收件人邮箱及密码
    user_tem = "qihuoxinhao01@163.com"
    password = 'A1234567'

    # 指定发件人
    users = ['WebStockWh8@wenhua.com.cn', '3405987953@qq.com', '1364826576@qq.com', '1410000000@qq.com']
    # 刷新时间间隔
    time_s = 1

    eamil_server = 'pop.163.com'

    email_class = down_email(user=user_tem, password=password, eamil_server=eamil_server)

    while 1:
        try:
            email_class.run_ing(users, time_s)
            time.sleep(time_s)
        except Exception as e:
            print("出现异常 切换用户中")


if __name__ == '__main__':
    # main()
    import zmail

    print(
        b"\xbd\xab\xbc\xec\xb2\xe2\xb5\xc4\xca\xb1\xbc\xe4\xbc\xe4\xb8\xf4\xb5\xf7\xb4\xf3\xd2\xbb\xd0\xa9\xa3\xac\xc0\xfd\xc8\xe75\xb7\xd6\xd6\xd3\xbc\xe0\xb2\xe2\xd2\xbb\xb4\xce".decode(
            "gb2312"))
    server = zmail.server('qihuoxinhao01@163.com', 'A1234567')
    number, size = server.stat()
    while 1:
        # 输入账号和密码
        new_number, new_size = server.stat()
        # 获取最新的一封邮件
        if new_number > number:
            number = new_number
            mail = server.get_latest()
            # 读取邮件
            zmail.show(mail)
            # 读取邮件的部分内容
            print(mail['subject'])
