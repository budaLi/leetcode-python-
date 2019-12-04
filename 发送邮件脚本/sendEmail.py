import smtplib  # 发送邮件 连接邮件服务器
from email.mime.text import MIMEText  # 构建邮件格式


class SendEmail:
    def __init__(self):
        # 发件人
        self.send_user = "李晋军" + "<1364826576@qq.com>"
        # 登录名
        self.login_user = '1364826576@qq.com'
        # 这里要注意 不是qq密码 而是在邮箱里设置的发送邮箱的授权码
        self.password = 'btfixrcdeguejfja'
        # 发送邮件的服务器地址 qq为smtp.qq.com  163邮箱为smtp.163.com
        self.email_host = 'smtp.qq.com'

    def send_email(self, userlist, subject, content):
        message = MIMEText(content, _subtype='plain', _charset='utf-8')
        message['Subject'] = subject
        message['From'] = self.send_user
        message['To'] = ';'.join(userlist)  # 收件人列表以分号隔开
        # 实例化邮件发送服务器
        server = smtplib.SMTP()
        # 连接qq邮箱服务器
        server.connect(self.email_host)
        # 登录服务器
        server.login(self.login_user, self.password)
        # 发送邮件  注意此处消息的格式应该用as_string()函数
        server.sendmail(self.send_user, userlist, message.as_string())
        # 关闭邮箱
        server.close()

    def send_test(self, userlist, passNumber, failNumber):
        """
        发送测试结果
        :param userlist:
        :param passNumber:
        :param failNumber:
        :return:
        """
        totalNumber = passNumber + failNumber

        # %.2f表示保留小数点后两位小数 %%表示百分之百
        passPercentage = "%.2f%%" % (passNumber / totalNumber * 100)
        failPercentae = "%.2f%%" % (failNumber / totalNumber * 100)

        sub = "测试结果报告"
        content = " 测试用例总数\t%s个\n通过个数\t%s个\n失败个数\t%s个\n通过率\t%s\n失败率\t%s" % (
            totalNumber, passNumber, failNumber, passPercentage, failPercentae)
        self.send_email(userlist, sub, content)
        return True


if __name__ == "__main__":
    send = SendEmail()
    user_list = ['1364826576@qq.com']
    send.send_test(user_list, 4, 5)
