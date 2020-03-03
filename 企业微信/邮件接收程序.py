# @Time    : 2020/2/28 13:30
# @Author  : Libuda
# @FileName: main.py
# @Software: PyCharm
# -*- coding: utf-8 -*-

import poplib
import time
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from 企业微信.config import get_config
import re

config = get_config()

def logger(msg):
    """
    日志信息
    """
    now = time.ctime()
    print("[%s] %s" % (now, msg))


class ReciveEmail():

    def __init__(self):

        # 收件人
        self.user = config['rev_user']

        # 指定发件人
        self.users = config['send_users'].split(",")

        # 输入邮件地址, 口令和POP3服务器地址:
        self.email_server = config['email_server']

        # 此处密码是授权码,用于登录第三方邮件客户端
        self.password = config['password']

        self.count = 0
        self.totle_set = None  # 邮件去重

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
            # print("这是text/xl")
            content = msg.get_payload(decode=True)
            # print("这是未解析正文", content)
            charset = self.guess_charset(msg)
            if charset:
                # print("编码格式",charset)
                content = content.decode("unicode-escape")
                # print("这是正文", content)
                # content = content.decode("utf-8")
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

    def run_ing(self):
        try:
            # telnetlib.Telnet(self.pop3_server, 995)
            self.server = poplib.POP3(self.email_server, 110, timeout=10)
        except Exception as e:
            print("服务器连接失败", e)
            self.server = poplib.POP3(self.email_server, 110, timeout=10)

        # 打印POP3服务器的欢迎文字:
        # print("身份验证成功，下面为测试输出：{}".format(self.server.getwelcome().decode('utf-8')))
        # 身份认证:
        self.server.user(self.user)
        self.server.pass_(self.password)
        # 返回邮件数量和占用空间:
        # logger('邮件总数: %s. 大小: %s' % self.server.stat())

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
                msg_content = b'\r\n'.join(lines).decode('gb2312')
            except Exception as  e:
                msg_content = b'\r\n'.join(lines).decode('utf-8')
                # 解析邮件:
                # print("解析前：",msg_content)
            # print("msg_content",msg_content)
            msg = Parser().parsestr(msg_content)
            # print("msg",msg)
            try:
                # 方法2：from or Form均可
                From = parseaddr(msg.get('From'))[1]
                To = parseaddr(msg.get('To'))[1]
                Cc = parseaddr(msg.get_all('Cc'))[1]  # 抄送人
                Subject = self.decode_str(msg.get('Subject'))
                # date1 = time.strptime(msg.get("Date")[0:24], '%a, %d %b %Y %H:%M:%S')

                # 邮件时间格式转换
                # date2 = time.strftime("%Y-%m-%d %H:%M:%S", date1)

                if From in self.users:
                    # print(date2,start_time)
                    # print("\n")
                    # print('发件人:%s,收件人:%s,抄送人:%s,主题:%s' % (From, To, Cc, Subject))
                    content = self.get_att(msg)
                    # print("邮件正文:{} \n".format(content))
                    return content

            except Exception as e:
                print(e, "解析错误")
                return None

        # 可以根据邮件索引号直接从服务器删除邮件:
        # self.server.dele(7)

        # 退出 不然会锁死
        self.server.quit()


def trans_content(coontent):
    # res_tem =
    content = "模组名: 沪铅主连_1分钟_金肯特纳(1)" \
              "模型名: 金肯特纳合约名: 沪铅主连   " \
              "周期: 1分钟14:57:58 [运行日志]14:57:58(本机时间): " \
              "信号30 平仓盈亏 -300 <合计 -1000>"

    # partten = re.compile(r"模组名.* $")
    # res = re.findall(partten,content)
    # print(res)


def get_rev():
    reciveemail = ReciveEmail()
    return reciveemail



if __name__ == '__main__':
    trans_content(1)
    # reciveemail= get_rev()
    # while 1:
    #     try:
    #         content = reciveemail.run_ing()
    #         print(content)
    #     except Exception as e:
    #         print("运行错误",e)
