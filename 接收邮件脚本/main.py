# @Time    : 2020/2/28 13:30
# @Author  : Libuda
# @FileName: 远程服务器文件监控.py
# @Software: PyCharm
# -*- coding: utf-8 -*-

import poplib, email, telnetlib
import datetime, time, sys, traceback
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr


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


    def connect_server(self):
        pass

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
        try:
            # telnetlib.Telnet(self.pop3_server, 995)
            self.server = poplib.POP3(self.pop3_server, 110, timeout=10)
        except Exception as e:
            print("链接错误", e)
            try:
                self.server = poplib.POP3(self.pop3_server, 110, timeout=10)
            except Exception as e:
                print("123", e)
        self.server.user(self.user)
        self.server.pass_(self.password)
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
            print(i, lines)
            # lines存储了邮件的原始文本的每一行,
            # 邮件的原始文本:
            try:
                msg_content = b"".join(lines).decode('utf-8')
                # 解析邮件:
                msg = Parser().parsestr(msg_content)

                print("msg", msg)
            except Exception as e:
                print("1", e)
                print(type(lines), lines)
                # print(b''.join(lines))

            try:
                # 方法2：from or Form均可
                From = parseaddr(msg.get('from'))[1]
                print("form", From)
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
            except Exception as e:
                print("解析出错", e)



        # 可以根据邮件索引号直接从服务器删除邮件:
        # self.server.dele(7)
        self.server.quit()


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

    eamil_server = 'pop3.chengxuhua.cc'
    user = user_lis.pop(0)
    user_lis.append(user)
    email_class = down_email(user=user, password=password, eamil_server=eamil_server)

    while 1:
        try:
            print("当前使用用户：{}".format(user))
            time.sleep(time_s)
            email_class.run_ing(users, time_s)
        except Exception as e:
            print("456", e)
            print("出现异常 切换用户中")
            user = user_lis.pop(0)
            user_lis.append(user)
            email_class = down_email(user=user, password=password, eamil_server=eamil_server)


def test():
    # 收件人邮箱及密码
    user_tem = "admin@chengxuhua.cc"
    password = 'A1234567'

    # 指定发件人
    users = ['WebStockWh8@wenhua.com.cn', '3405987953@qq.com', '1364826576@qq.com', '1410000000@qq.com']
    # 刷新时间间隔
    time_s = 1

    eamil_server = 'pop3.chengxuhua.cc'

    email_class = down_email(user=user_tem, password=password, eamil_server=eamil_server)

    while 1:
        try:
            email_class.run_ing(users, time_s)
            time.sleep(time_s)
        except Exception as e:
            print(e)
            print("出现异常 切换用户中")


if __name__ == '__main__':
    test()
    # s= [b'Return-Path: 1364826576@qq.com', b'Received: from qq.com (smtpbg407.qq.com [113.96.223.67])', b'\tby EBS-39933 with ESMTP', b'\t; Mon, 2 Mar 2020 16:42:36 +0800', b'DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed; d=qq.com; s=s201512;', b'\tt=1583138557; bh=ClxYRsg4hBJKTkGmb5CJ3iiiRUV8zPoacHdPERtDIcU=;', b'\th=From:To:Subject:Mime-Version:Date:Message-ID;', b'\tb=Bi2SZmz+BwifRqbBqUSzmvX8vbyybB9upBUioFKnj0YJfHQZO4FiUnx5LeJw76aJW', b'\t tR/DXsHUcVYiJ9cMYaF0hbAJg5Eo9gDLxnHRAohVr+rK4MrTKKhuVrIsg7XqOihhlH', b'\t P8fua4OCNJjBLnojmJDwOQAS92APTQq8crwLmzms=', b'X-QQ-FEAT: akyE7Jl3ukrXCJ4nsNQlU1b+Ip+IhAjXCMr84XXeRusNXKtkQleoiiExYPSWW', b'\tXlqvR4bHspnQL7e4XS9g2J0hwb7+JoI12gSR8ayLoI4drtLdb+dII+L9/9wV/L3oALN0fg0', b'\t5zVwaPQqU4VdUFTNg0cAZnb777tkQeMPbBF2xT+Lrv4J4Cn3XEblR9oJPBt9d21CZT/I6ve', b'\tVxRfNmfBmIPOH9X8jfz/CWcPoU1YFl/o1t0CtS9vx6d51DgDfM5bm9vEShZ4OnhY=', b'X-QQ-SSF: 000000000000003000000000000000Z', b'X-HAS-ATTACH: no', b'X-QQ-BUSINESS-ORIGIN: 2', b'X-Originating-IP: 36.110.255.206', b'X-QQ-STYLE: ', b'X-QQ-mid: webmail501t1583138555t942617', b'From: "=?ISO-8859-1?B?MTM2NDgyNjU3Ng==?=" <1364826576@qq.com>', b'To: "=?ISO-8859-1?B?YWRtaW4=?=" <admin@chengxuhua.cc>', b'Subject: 44', b'Mime-Version: 1.0', b'Content-Type: multipart/alternative;', b'\tboundary="----=_NextPart_5E5CC6FB_0FD4DB58_2A514D2E"', b'Content-Transfer-Encoding: 8Bit', b'Date: Mon, 2 Mar 2020 16:42:35 +0800', b'X-Priority: 3', b'Message-ID: <tencent_FA99D04CCB8B2CBAAFEB43525AD692316D07@qq.com>', b'X-QQ-MIME: TCMime 1.0 by Tencent', b'X-Mailer: QQMail 2.x', b'X-QQ-Mailer: QQMail 2.x', b'X-QQ-SENDSIZE: 520', b'Received: from qq.com (unknown [127.0.0.1])', b'\tby smtp.qq.com (ESMTP) with SMTP', b'\tid ; Mon, 02 Mar 2020 16:42:36 +0800 (CST)', b'Feedback-ID: webmail:qq.com:bgweb:bgweb15', b'', b'This is a multi-part message in MIME format.', b'', b'------=_NextPart_5E5CC6FB_0FD4DB58_2A514D2E', b'Content-Type: text/plain;', b'\tcharset="ISO-8859-1"', b'Content-Transfer-Encoding: base64', b'', b'NA==', b'', b'------=_NextPart_5E5CC6FB_0FD4DB58_2A514D2E', b'Content-Type: text/html;', b'\tcharset="ISO-8859-1"', b'Content-Transfer-Encoding: base64', b'', b'PG1ldGEgaHR0cC1lcXVpdj0iQ29udGVudC1UeXBlIiBjb250ZW50PSJ0ZXh0L2h0bWw7IGNo', b'YXJzZXQ9R0IxODAzMCI+PGRpdj40PC9kaXY+', b'', b'------=_NextPart_5E5CC6FB_0FD4DB58_2A514D2E--', b'']
    # print(b"".join(s).decode("utf-8"))
