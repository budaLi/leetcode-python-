import re
import werobot
import xlrd
import smtplib  # 发送邮件 连接邮件服务器
from email.mime.text import MIMEText  # 构建邮件格式
from xlutils.copy import copy
from selenium import webdriver
import time
import datetime
from config import get_config
from selenium.webdriver.chrome.options import Options
import pandas as pd
from pandas import DataFrame
from copy import deepcopy

robot = werobot.WeRoBot(token='fandengdushu')
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument(
    'user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')
chrome_options.add_argument('--no-sandbox')  # 这个配置很重要

config = get_config()
# driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=config['executable_path'])
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="/usr/bin/chromedriver")

user_list = ['1364826576@qq.com']

phone_num = 13281890000
wait_time = 0.5  # 各个阶段等待时间
time_jiange = 30  # 时间间隔 隔多长时间执行脚本一次
start_date = datetime.datetime.strptime("2019-12-1 00:00:00", "%Y-%m-%d %H:%M:%S")  # 起始时间
end_date = datetime.datetime.strptime("2019-12-13 18:00:00", "%Y-%m-%d %H:%M:%S")  # 结束时间
ding_num = 5  # 链接条数报警阈值
# 更换头部

# driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='/usr/bin/chromedriver')
# driver = webdriver.Chrome(config['executable_path'],options=chrome_options)

link_file_path = config['link_file_path']
# phone_file_path = config['phone_file_path']

link_ecel = xlrd.open_workbook(link_file_path)
link_tables = link_ecel.sheet_by_index(0)
link_get_col = 2
link_write_col = 3

# phone_excel = xlrd.open_workbook(phone_file_path)
# phoe_tables = phone_excel.sheet_by_index(0)
# phone_get_col = 1
# phone_write_col = 2

# phone_can_use_index = phoe_tables.get_rows()
link_can_use_index = int(config['start_link_index'])
totle_break_set = set()


def logger(msg):
    """
    日志信息
    """
    now = time.ctime()
    print("[%s] %s" % (now, msg))


def get_keywords_data(tables, row, col):
    actual_data = tables.cell_value(row, col)
    return actual_data


def write_to_excel(file_path, row, col, value):
    work_book = xlrd.open_workbook(file_path, formatting_info=False)
    write_to_work = copy(work_book)
    sheet_data = write_to_work.get_sheet(0)
    sheet_data.write(row, col, str(value))
    write_to_work.save(file_path)


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

    def send_test(self, userlist, counts):
        """
        发送测试结果
        :param userlist:
        :param passNumber:
        :param failNumber:
        :return:
        """

        sub = "链接剩余条数预警"
        content = "链接剩余:{}条".format(counts)
        self.send_email(userlist, sub, content)
        return True


send = SendEmail()


def register(phone):
    """
    给手机号开卡 返回开卡结果及剩余链接数
    :param phone:
    :return:
    """
    res = None
    df = pd.read_excel(link_file_path)
    link_data = []
    for i in df.index.values:  # 获取行号的索引，并对其进行遍历：
        # 根据i来获取每一行指定的数据 并利用to_dict转成字典
        row_data = df.loc[i, ['id', 'link']].to_dict()
        link_data.append(row_data)

    link_data_tem = deepcopy(link_data)
    writer = pd.ExcelWriter(link_file_path, cell_overwrite_ok=True)
    dataframe = DataFrame()
    for index, data in enumerate(link_data):
        link = (data['link'])

        driver.get(link)
        time.sleep(wait_time)
        try:
            text = driver.find_element_by_xpath("/html/body/div[1]/div[1]/p[1]")
            if text.text == "开卡失败":
                write_to_excel(link_file_path, index + 1, link_write_col, "已使用")
                print("该卡已经被使用..{}".format(link))
                link_data_tem.pop(0)
                continue
        except Exception as e:
            pass
            # time.sleep(wait_time)
            # # print(e)
        try:
            print("该卡可以使用:{}，正在查询可用手机号。。".format(link))
            text = driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/p')

            if text.text == "欢迎加入樊登读书，即刻获得":
                driver.get(link)
                time.sleep(wait_time)
                driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[1]/input').send_keys(phone)
                driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[3]/input').send_keys(phone)
                driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[3]').click()
                time.sleep(wait_time)
                # 点击开卡
                driver.find_element_by_xpath('//*[@id="join-btn"]').click()
                # 点击开卡后页面延迟较为严重
                time.sleep(wait_time)
                try:
                    tem = driver.find_element_by_xpath('/html/body/div[1]/div[1]/p[1]')
                    if tem.text == "开卡失败":
                        res = "开卡失败"
                        print("开卡失败，您已经是樊登读书好友")

                except Exception as e:
                    time.sleep(wait_time)
                    try:
                        if driver.find_element_by_xpath('/html/body/div[1]/div/h1').text == "领取成功！":
                            print("开卡成功")
                            res = "开卡成功"
                            link_data_tem.pop(0)
                    except Exception as e:
                        print("此电话号码有问题")
                        res = "此电话号码有问题"


        except Exception as e:
            print(e)

        if len(link_data_tem) <= 0:
            link_data_tem = [{"id": "", "link": ""}]

        dataframe = dataframe.append(DataFrame(link_data_tem))
        dataframe.to_excel(writer, index=0)
        writer.save()
        return res, len(link_data_tem)


# 被关注自动回复
@robot.subscribe
def subscribe(message):
    return "樊登读书14天VIP免费领\n" + "回复手机号自动领取……\n" + "\n\n客服微信：95499954\n（找客服免费领取最新整理书单）"


# 接受信息自动回复
@robot.handler
def echo(message):
    message = message.content
    ret = re.match(r"^1[35678]\d{9}$", message)
    if ret:
        print("手机号验证成功")
        try:
            return "请耐心等候，正在查询您的开卡状态，为开卡将自动为您开卡"
        except Exception:
            return "请耐心等候，正在查询您的开卡状态，为开卡将自动为您开卡"
        finally:
            # res,lenght = register(message)
            # print(res,lenght)
            # return res,lenght
            res = "ss"
            lenght = "s"
            # try:
            #     return ("开卡信息:{}","剩余14天VIP卡数量“{}”张".format(res,lenght))
            # except Exception as e:
            #     print(e)
            #
            return "开卡信息:{},剩余14天VIP卡数量“{}”张".format(res, lenght)
    try:
        with open("1", encoding="utf-8") as f:
            data = ".".join(f.readlines())
    except Exception:
        data = "此文件不在 请创建:{}".format("1")
    return data


if __name__ == '__main__':
    robot.config['HOST'] = '0.0.0.0'
    robot.config['PORT'] = 80

    robot.run()
