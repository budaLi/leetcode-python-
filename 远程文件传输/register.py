# @Time    : 2020/3/15 18:57
# @Author  : Libuda
# @FileName: register.py
# @Software: PyCharm
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
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=config['executable_path'])
# driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="/usr/bin/chromedriver")
#
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


def register(phone):
    """
    给手机号开卡 返回开卡结果及剩余链接数
    :param phone:
    :return:
    """
    print("开卡中")
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
            time.sleep(wait_time)
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
                        if len(link_data_tem) <= 0:
                            link_data_tem = [{"id": "", "link": ""}]

                        dataframe = dataframe.append(DataFrame(link_data_tem))
                        dataframe.to_excel(writer, index=0)
                        writer.save()
                        return res, len(link_data_tem)
                except Exception as e:
                    print(e)
                    time.sleep(wait_time)
                    try:
                        if driver.find_element_by_xpath('/html/body/div[1]/div/h1').text == "领取成功！":
                            print("开卡成功")
                            res = "开卡成功"
                            link_data_tem.pop(0)
                            if len(link_data_tem) <= 0:
                                link_data_tem = [{"id": "", "link": ""}]

                            dataframe = dataframe.append(DataFrame(link_data_tem))
                            dataframe.to_excel(writer, index=0)
                            writer.save()
                            return res, len(link_data_tem)
                    except Exception as e:
                        print(e)
                        res = e
                        if len(link_data_tem) <= 0:
                            link_data_tem = [{"id": "", "link": ""}]

                        dataframe = dataframe.append(DataFrame(link_data_tem))
                        dataframe.to_excel(writer, index=0)
                        writer.save()
                        return res, len(link_data_tem)


        except Exception as e:
            print(e)

        # if len(link_data_tem) <= 0:
        #     link_data_tem = [{"id": "", "link": ""}]
        #
        # dataframe = dataframe.append(DataFrame(link_data_tem))
        # dataframe.to_excel(writer, index=0)
        # writer.save()
    return res, len(link_data_tem)


if __name__ == '__main__':
    res, l = register("15735656005")
    print(res, l)
