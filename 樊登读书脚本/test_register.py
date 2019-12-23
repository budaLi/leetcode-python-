# @Time    : 2019/12/11 10:09
# @Author  : Libuda
# @FileName: test_register.py
# @Software: PyCharm
import xlrd
import smtplib  # 发送邮件 连接邮件服务器
from email.mime.text import MIMEText  # 构建邮件格式
from xlutils.copy import copy
from selenium import webdriver
import time
import datetime
from configparser import ConfigParser

config_parser = ConfigParser()
config_parser.read('config.cfg', encoding="utf-8-sig")
config = config_parser['default']

user_list = ['1364826576@qq.com']

phone_num = 13281890000
wait_time = 3  # 各个阶段等待时间
time_jiange = 30  # 时间间隔 隔多长时间执行脚本一次
start_date = datetime.datetime.strptime("2019-12-1 00:00:00", "%Y-%m-%d %H:%M:%S")  # 起始时间
end_date = datetime.datetime.strptime("2019-12-13 18:00:00", "%Y-%m-%d %H:%M:%S")  # 结束时间
ding_num = 5  # 链接条数报警阈值
# 更换头部
options = webdriver.ChromeOptions()
mobile_emulation = {
    "deviceMetrics": {"width": 414, "height": 736, "pixelRatio": 3.0},
    "userAgent": "mozilla/5.0 (linux; u; android 4.1.2; zh-cn; mi-one plus build/jzo54k) applewebkit/534.30 (khtml, like gecko) version/4.0 mobile safari/534.30 micromessenger/5.0.1.352"}

# 设置图片不加载
prefs = {
    'profile.default_content_setting_values': {
        'images': 2
    }
}

options.add_experimental_option("mobileEmulation", mobile_emulation)
options.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome(config['executable_path'])
link_file_path = config['link_file_path']
phone_file_path = config['phone_file_path']

link_ecel = xlrd.open_workbook(link_file_path)
link_tables = link_ecel.sheet_by_index(0)
link_get_col = 2
link_write_col = 3

phone_excel = xlrd.open_workbook(phone_file_path)
phoe_tables = phone_excel.sheet_by_index(0)
phone_get_col = 1
phone_write_col = 2

phone_can_use_index = phoe_tables.get_rows()
link_can_use_index = int(config['start_link_index'])
totle_break_set = set()


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


def register(phone_data):
    global phone_can_use_index, link_can_use_index, ding_num
    phone_excel = xlrd.open_workbook(phone_file_path)
    phoe_tables = phone_excel.sheet_by_index(0)
    phone_can_use_index = phoe_tables.nrows
    link_data = [get_keywords_data(link_tables, i, link_get_col) for i in range(link_can_use_index, link_tables.nrows)]
    length = len(phone_data)
    phone_index = 0
    has_phone = True
    for index, link in enumerate(link_data):
        if len(link_data) <= ding_num:
            print("当前链接条数为：{}，当前链接条数不足 请及时补充！".format(len(link_data)))
            send.send_test(user_list, len(link_data))
        if length <= 0:
            print("当前手机号已全被使用")
            break
        ding_num -= 1
        if has_phone:
            driver.get(link)
            time.sleep(wait_time)
            try:
                text = driver.find_element_by_xpath("/html/body/div[1]/div[1]/p[1]")
                if text.text == "开卡失败":
                    write_to_excel(link_file_path, index + 1, link_write_col, "已使用")
                    print("该卡已经被使用..{}".format(link))
                    link_can_use_index += 1
                    continue
                else:
                    write_to_excel(link_file_path, index + 1, link_write_col, "已使用")
                    print("该卡已经被使用..{}".format(link))
                    link_can_use_index += 1
                    continue
            except Exception as e:
                time.sleep(wait_time)
                # print(e)
            try:
                print("该卡可以使用:{}，正在查询可用手机号。。".format(link))
                text = driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/p')

                if text.text == "欢迎加入樊登读书，即刻获得":
                    flag = True
                    while flag:
                        for ph_number_index in range(phone_index, len(phone_data)):
                            driver.get(link)
                            length -= 1
                            phone_index += 1
                            print("当前查询手机号索引为{}，号码为{}".format(ph_number_index, phone_data[ph_number_index][0]))
                            time.sleep(wait_time)
                            driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[1]/input').send_keys(
                                phone_data[ph_number_index][0])
                            driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[3]/input').send_keys(
                                phone_data[ph_number_index][0])
                            driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[3]').click()
                            time.sleep(wait_time)
                            # 点击开卡
                            driver.find_element_by_xpath('//*[@id="join-btn"]').click()
                            # 点击开卡后页面延迟较为严重
                            time.sleep(wait_time)
                            try:
                                tem = driver.find_element_by_xpath('/html/body/div[1]/div[1]/p[1]')
                                if tem.text == "开卡失败":
                                    print("开卡失败，您已经是樊登读书好友")

                                    # 日期
                                    write_to_excel(phone_file_path, phone_can_use_index + 1, phone_write_col - 2,
                                                   phone_data[ph_number_index][1])
                                    # 手机号
                                    write_to_excel(phone_file_path, phone_can_use_index + 1, phone_write_col - 1,
                                                   phone_data[ph_number_index][0])
                                    # 使用状态
                                    write_to_excel(phone_file_path, phone_can_use_index + 1, phone_write_col,
                                                   "开卡失败您已经是樊登读书书友")
                                    phone_can_use_index += 1
                            except Exception as e:
                                # print(e)
                                flag = False
                                time.sleep(wait_time)
                                try:
                                    if driver.find_element_by_xpath('/html/body/div[1]/div/h1').text == "领取成功！":
                                        print("开卡成功")
                                        write_to_excel(link_file_path, index + 1, link_write_col, "领取成功")
                                        # 日期
                                        write_to_excel(phone_file_path, phone_can_use_index + 1, phone_write_col - 2,
                                                       phone_data[ph_number_index][1])
                                        # 手机号
                                        write_to_excel(phone_file_path, phone_can_use_index + 1, phone_write_col - 1,
                                                       phone_data[ph_number_index][0])
                                        # 使用状态
                                        write_to_excel(phone_file_path, phone_can_use_index + 1, phone_write_col,
                                                       "领取成功")
                                        link_can_use_index += 1
                                        phone_can_use_index += 1
                                        has_phone = True
                                        break
                                except Exception as e:
                                    print("此电话号码有问题")
                                    # write_to_excel(link_file_path, index + 1, link_write_col, "此电话号码有问题")
                                    write_to_excel(link_file_path, index + 1, link_write_col, "领取成功")
                                    # 日期
                                    write_to_excel(phone_file_path, phone_can_use_index + 1, phone_write_col - 2,
                                                   phone_data[ph_number_index][1])
                                    # 手机号
                                    write_to_excel(phone_file_path, phone_can_use_index + 1, phone_write_col - 1,
                                                   phone_data[ph_number_index][0])
                                    # 使用状态
                                    write_to_excel(phone_file_path, phone_can_use_index + 1, phone_write_col,
                                                   "此电话号码有问题")
                                    # write_to_excel(phone_file_path, phone_can_use_index + 1, phone_write_col, "此电话号码有问题")
                                    phone_can_use_index += 1
                                    has_phone = True
                                    continue
                                    # print(e)
                        flag = False
                else:
                    # print(text.text)
                    continue
            except Exception as e:
                pass

    # 发邮件
    send.send_test(user_list, 0)
    print("链接已经全部用完 请及时补充！")
    # print(e)


if __name__ == '__main__':
    user_agent = "mozilla/5.0 (linux; u; android 4.1.2; zh-cn; mi-one plus build/jzo54k) applewebkit/534.30 (khtml, like gecko) version/4.0 mobile safari/534.30 micromessenger/5.0.1.352"
    phone_len = phoe_tables.nrows
    print("手机号共：{}个".format(phone_len))
    phone_data = []
    for i in range(phone_len):
        phone_data.append([get_keywords_data(phoe_tables, i, phone_get_col), 0])
    y = input("是否设置完毕")
    register(phone_data)
