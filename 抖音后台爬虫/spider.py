# @Time    : 2019/11/25 16:55
# @Author  : Libuda
# @FileName: 加密spider.py
# @Software: PyCharm

import pandas
import time
from selenium import webdriver

driver = webdriver.Chrome(r'C:\Users\lenovo\PycharmProjects\Spider\chromedriver.exe')
file_path = r"C:\Users\lenovo\PycharmProjects\leetcode-python-\抖音后台爬虫\res.xls"
df = pandas.DataFrame()
driver.get("https://e.douyin.com/site/")
print("请您进行登录及手动进行所有的筛选")
yes = input("您是否已确认进行爬取")
if yes == "y":
    all_data_len = driver.find_element_by_xpath(
        '//*[@id="root"]/div/div[2]/div[1]/div/div/div[3]/div[1]/div[2]/div[3]/div/div/div/div/div/ul/li[1]').text.split(
        "条")[0].split("共")[1]
    print("总共 {} 条数据".format(all_data_len))

    num_tem = '//*[@id="root"]/div/div[2]/div[1]/div/div/div[3]/div[1]/div[2]/div[3]/div/div/div/div/div/div/div/div[1]/div/table/tbody/tr[{}]/td[4]/div'
    # num_tem = '//*[@id="root"]/div[2]/div[1]/div/div/div[3]/div[1]/div[2]/div[3]/div/div/div/div/div/div/div/div[1]/div/table/tbody/tr[{}]/td[4]'
    date_tem = '//*[@id="root"]/div/div[2]/div[1]/div/div/div[3]/div[1]/div[2]/div[3]/div/div/div/div/div/div/div/div[1]/div/table/tbody/tr[{}]/td[6]/div'
    # num_tem = '//*[@id="root"]/div[2]/div[1]/div/div/div[3]/div[1]/div[2]/div[3]/div/div/div/div/div/div/div/div[1]/div/table/tbody/tr[{}]/td[4]'
    # date_tem = '//*[@id="root"]/div[2]/div[1]/div/div/div[3]/div[1]/div[2]/div[3]/div/div/div/div/div/div/div/div[1]/div/table/tbody/tr[{}]/td[6]'

    while len(df) < int(all_data_len):
        time.sleep(3)  # 时间间隔
        res_data = []
        for i in range(1, 11):
            try:
                res_dic = {}
                res_dic['phone_number'] = driver.find_element_by_xpath(num_tem.format(i)).text
                res_dic['date'] = driver.find_element_by_xpath(date_tem.format(i)).text
                res_data.append(res_dic)
            except Exception:
                pass
        df = df.append(res_data)
        df.to_excel(file_path, index=0)
        # 点击下一页
        try:
            driver.find_element_by_css_selector('.ant-pagination-next > a').click()
        except Exception as e:
            try:
                driver.find_element_by_css_selector('.ant-pagination-next > a').click()
            except Exception:
                pass
