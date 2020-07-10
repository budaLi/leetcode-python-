import smtplib  # 发送邮件 连接邮件服务器
from email.mime.text import MIMEText  # 构建邮件格式
from email.mime.multipart import MIMEMultipart  # 发送多个部分
from email.mime.image import MIMEImage  # 图片格式
from email.mime.application import MIMEApplication  # 发送附件

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

    def _send(self, userlist, message):
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

    def send_text(self, userlist, subject, content):
        """
        发送文本邮件
        :param userlist: 接收人  列表形式
        :param subject: 主题
        :param content:  内容
        :return:
        """
        message = MIMEText(content, _subtype='plain', _charset='utf-8')
        message['Subject'] = subject
        message['From'] = self.send_user
        message['To'] = ';'.join(userlist)  # 收件人列表以分号隔开
        self._send(userlist, message)

    def send_image(self, userlist, subject, img_path):
        """
        发送图片
        :param userlist:收件人列表
        :param subject:主题
        :param img_path:图片路径
        :return:
        """
        message = MIMEMultipart('related')
        content = MIMEText('<html><body><img src="cid:imageid" alt="imageid"></body></html>', 'html', 'utf-8')  # 正文
        message.attach(content)
        message['Subject'] = subject
        message['From'] = self.send_user
        message['To'] = ';'.join(userlist)  # 收件人列表以分号隔开

        file = open(img_path, "rb")
        img_data = file.read()
        file.close()

        img = MIMEImage(img_data)
        img.add_header('Content-ID', 'imageid')
        message.attach(img)

        self._send(userlist, message)

    def send_vedio(self, userlist, subject, file):
        """
        发送文件
        """
        message = MIMEMultipart('related')
        content = MIMEText('<html><body><img src="cid:imageid" alt="imageid"></body></html>', 'html', 'utf-8')  # 正文
        message.attach(content)
        message['Subject'] = subject
        message['From'] = self.send_user
        message['To'] = ';'.join(userlist)  # 收件人列表以分号隔开

        part_attach1 = MIMEApplication(open(file, 'rb').read())  # 打开附件
        part_attach1.add_header('Content-Disposition', 'attachment', filename=file)  # 为附件命名
        message.attach(part_attach1)  # 添加附件

        self._send(userlist, message)

if __name__ == "__main__":
    send = SendEmail()
    user_list = ['1364826576@qq.com']
    send.send_vedio(user_list, "图片", "1.jpeg")
    # send.send_text(user_list, 4, 5)
