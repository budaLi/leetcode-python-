# @Time    : 2019/12/2 11:17
# @Author  : Libuda
# @FileName: 加密spider.py
# @Software: PyCharm
import xlrd
import smtplib  # 发送邮件 连接邮件服务器
from email.mime.text import MIMEText  # 构建邮件格式
from xlutils.copy import copy
from selenium import webdriver
import time
import datetime
from configparser import ConfigParser
import copy as deepcopy

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


def get_keywords_data(tables, row, col):
    actual_data = tables.cell_value(row, col)
    return actual_data

def write_to_excel(file_path, row, col, value):
    work_book = xlrd.open_workbook(file_path, formatting_info=False)
    write_to_work = copy(work_book)
    sheet_data = write_to_work.get_sheet(0)
    sheet_data.write(row, col, str(value))
    write_to_work.save(file_path)


def get_phone_number(star_date, end_date):
    print("当前已使用手机号：{}，使用数量：{}".format(totle_break_set, len(totle_break_set)))
    result = []
    # 搜索按钮
    try:
        driver.find_element_by_xpath(
            '//*[@id="root"]/div[2]/div[1]/div/div/div[3]/div[1]/div[2]/div[2]/div[4]/span[2]/span/span').click()
    except Exception as e:
        pass

    # all_data_len = driver.find_element_by_xpath('//*[@id="root"]/div[2]/div[1]/div/div/div[3]/div[1]/div[2]/div[3]/div/div/div/div/div/ul/li[1]').text.split("条")[0].split("共")[1]
    # print("总共 {} 条数据".format(all_data_len))
    num_tem = '//*[@id="root"]/div/div[2]/div[1]/div/div/div[3]/div[1]/div[2]/div[3]/div/div/div/div/div/div/div/div[1]/div/table/tbody/tr[{}]/td[4]/div'
    # num_tem = '//*[@id="root"]/div[2]/div[1]/div/div/div[3]/div[1]/div[2]/div[3]/div/div/div/div/div/div/div/div[1]/div/table/tbody/tr[{}]/td[4]'
    date_tem = '//*[@id="root"]/div/div[2]/div[1]/div/div/div[3]/div[1]/div[2]/div[3]/div/div/div/div/div/div/div/div[1]/div/table/tbody/tr[{}]/td[6]/div'
    # date_tem = '//*[@id="root"]/div[2]/div[1]/div/div/div[3]/div[1]/div[2]/div[3]/div/div/div/div/div/div/div/div[1]/div/table/tbody/tr[{}]/td[6]'
    flag = True
    while flag:

        time.sleep(wait_time)  # 时间间隔
        for i in range(1, 11):
            res_dic = {}
            try:
                res_dic['phone_number'] = driver.find_element_by_xpath(num_tem.format(i)).text
                res_dic['date'] = datetime.datetime.strptime(driver.find_element_by_xpath(date_tem.format(i)).text,
                                                             "%Y.%m.%d %H:%M:%S")

                if res_dic['date'] < star_date or res_dic['date'] > end_date:
                    flag = False
                    break
                else:
                    if (res_dic['phone_number'],res_dic['date']) not in totle_break_set:
                        totle_break_set.add((res_dic['phone_number'],res_dic['date']))
                        result.append([res_dic['phone_number'], res_dic['date']])
                        # print("已获取手机号：{}".format(res_dic['phone_number']))
                    else:
                        flag = False
                        break
                        # pass


            except Exception as e :
                # print(e)
                flag = False
                break
        try:
            #这儿要处理
            driver.find_element_by_css_selector('.ant-pagination-next > a').click()
            time.sleep(wait_time)
        except Exception as e:
            print(e)
            # try:
            #     driver.find_element_by_xpath(
            #         '//*[@id="root"]/div[2]/div[1]/div/div/div[3]/div[1]/div[2]/div[3]/div/div/div/div/div/ul/li[12]').click()
            # except Exception as e:
            #     print(e)
            #     try:
            #         driver.find_element_by_xpath(
            #             '//*[@id="root"]/div[2]/div[1]/div/div/div[3]/div[1]/div[2]/div[3]/div/div/div/div/div/ul/li[10]').click()
            #     except Exception as e:
            #         print(e)
            #         flag = False

    tem_break = deepcopy.deepcopy(totle_break_set)
    print("已爬取到新手机号：{}个".format(len(result)))
    print("翻页结束,等待页数回滚中。。。")
    pre_flag = True
    while pre_flag:
        try:
            for i in range(10):
                tem_break.pop()
            driver.find_element_by_css_selector('.ant-pagination-prev > a').click()
            # driver.find_element_by_xpath(
            #     '//*[@id="root"]/div/div[2]/div[1]/div/div/div[3]/div[1]/div[2]/div[3]/div/div/div/div/div/ul/li[2]/a').click()
            time.sleep(wait_time)
        except Exception as e:
            # print(e)
            pre_flag = False
            print("回滚结束")


    return result


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
        ding_num-=1
        if has_phone:
            driver.get(link)
            time.sleep(wait_time)
            try:
                text = driver.find_element_by_xpath("/html/body/div[1]/div[1]/p[1]")
                if text.text == "开卡失败":
                    write_to_excel(link_file_path, index + 1, link_write_col, "已使用")
                    print("该卡已经被使用..{}".format(link))
                    link_can_use_index+=1
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
                            phone_index+=1
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


def main():
    crawl_count = 1
    windows = ""
    second_window = ''
    while 1:

        # time_str = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        # print(times)
        # # s="2019.12.02 13:56:20"
        # # print(datetime.datetime.strptime(s,"%Y.%m.%d %H:%M:%S")<times)
        if crawl_count == 1:
            print("第1次爬取")
            # driver.get("https://e.douyin.com/site/manage-center/user-manage")
            driver.get("https://e.douyin.com/site/")

            print("请您进行登录及手动进行所有的筛选")
            yes = input("您是否已确认进行爬取")
            # cookie= driver.get_cookies()
            # driver.get("https://e.douyin.com/site/manage-center/user-manage")
            phone_data = get_phone_number(start_date, end_date)
            # print([phone for phone in phone_data[0]])
            windows = driver.current_window_handle
            js = 'window.open("https://www.baidu.com");'
            driver.execute_script(js)
            for wins in driver.window_handles:
                if wins != windows:
                    driver.switch_to.window(wins)
            second_window = driver.current_window_handle
            y = input("是否设置完毕")
            # 测试
            # phone_data = [[phone, 0] for phone in [13945868092, 15169722520]]
            register(phone_data)
            driver.switch_to.window(windows)

            crawl_count += 1
        else:
            print("第{}次爬取".format(crawl_count))
            phone_data = get_phone_number(start_date, end_date)
            driver.switch_to.window(second_window)
            register(phone_data)
            driver.switch_to.window(windows)
            crawl_count += 1

        time.sleep(time_jiange)


if __name__ == '__main__':
    #主函数
    main()
