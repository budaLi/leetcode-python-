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


class down_email():

    def __init__(self, user, password, eamil_server):
        # 输入邮件地址, 口令和POP3服务器地址:
        self.user = user
        # 此处密码是授权码,用于登录第三方邮件客户端
        self.password = password
        self.pop3_server = eamil_server

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
    def get_att(self, msg_in, str_day):
        result = []
        for part in msg_in.walk():
            # 是文本内容
            content = self.get_content(part)
            if content:
                result.append(content)
        return ",".join(result)

    def run_ing(self):
        str_day = str(datetime.date.today())  # 日期赋值
        print("获取时间：{}".format(str_day))
        # 连接到POP3服务器,有些邮箱服务器需要ssl加密，可以使用poplib.POP3_SSL
        try:
            telnetlib.Telnet(self.pop3_server, 995)
            self.server = poplib.POP3_SSL(self.pop3_server, 995, timeout=10)
        except:
            time.sleep(5)
            self.server = poplib.POP3(self.pop3_server, 110, timeout=10)
        # server.set_debuglevel(1) # 可以打开或关闭调试信息

        # 打印POP3服务器的欢迎文字:
        print("身份验证成功，下面为测试输出：{}".format(self.server.getwelcome().decode('utf-8')))
        # 身份认证:
        self.server.user(self.user)
        self.server.pass_(self.password)
        # 返回邮件数量和占用空间:
        print('邮件总数: %s. 大小: %s' % self.server.stat())

        # list()返回所有邮件的编号:
        resp, mails, octets = self.server.list()
        # 可以查看返回的列表类似[b'1 82923', b'2 2184', ...]
        # print(mails)

        index = len(mails)

        for i in range(index, 0, -1):  # 倒序遍历邮件

            # for i in range(1, index + 1):# 顺序遍历邮件
            resp, lines, octets = self.server.retr(i)
            # lines存储了邮件的原始文本的每一行,
            # 邮件的原始文本:
            msg_content = b'\r\n'.join(lines).decode('utf-8')
            # 解析邮件:
            msg = Parser().parsestr(msg_content)
            # 获取邮件的发件人，收件人， 抄送人,主题
            # hdr, addr = parseaddr(msg.get('From'))
            # From = self.decode_str(hdr)
            # hdr, addr = parseaddr(msg.get('To'))
            # To = self.decode_str(hdr)

            # 方法2：from or Form均可
            From = parseaddr(msg.get('from'))[1]
            To = parseaddr(msg.get('To'))[1]
            Cc = parseaddr(msg.get_all('Cc'))[1]  # 抄送人
            Subject = self.decode_str(msg.get('Subject'))
            print('发件人:%s,收件人:%s,抄送人:%s,主题:%s' % (From, To, Cc, Subject))
            # 获取邮件时间,格式化收件时间
            date1 = time.strptime(msg.get("Date")[0:24], '%a, %d %b %Y %H:%M:%S')
            # 邮件时间格式转换
            date2 = time.strftime("%Y-%m-%d", date1)
            if date2 < str_day:
                break  # 倒叙用break
                # continue # 顺叙用continue
            else:
                # 获取内容
                content = self.get_att(msg, str_day)
                print("邮件正文:{} \n".format(content))
        # 可以根据邮件索引号直接从服务器删除邮件:
        # self.server.dele(7)

        self.server.quit()


if __name__ == '__main__':
    try:
        # 输入邮件地址, 口令和POP3服务器地址:
        user = '15735656005@163.com'
        # 此处密码是授权码,用于登录第三方邮件客户端
        password = 'zslswmz1'
        eamil_server = 'pop.163.com'

        email_class = down_email(user=user, password=password, eamil_server=eamil_server)
        email_class.run_ing()

    except Exception as e:
        import traceback

        ex_msg = '{exception}'.format(exception=traceback.format_exc())
        print(ex_msg)
