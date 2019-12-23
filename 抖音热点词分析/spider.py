# @Time    : 2019/11/19 17:41
# @Author  : Libuda
# @FileName: 加密spider.py
# @Software: PyCharm

import time
import jieba
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('window-size=1200,1100')
driver = webdriver.Chrome(chrome_options=chrome_options,
                          executable_path=r'C:\Users\lenovo\PycharmProjects\Spider\chromedriver.exe')
driver.get("https://www.iesdouyin.com/share/billboard/")
time.sleep(5)
redian_base_xpath = "/html/body/div[2]/div[1]/div[3]/div[3]/div[{}]/div[1]/div[2]/span[1]"
redian_dic = {}
vedio_dic = {}
count = 1
while 1:
    try:
        data = driver.find_element_by_xpath(redian_base_xpath.format(str(count)))
        seg_list = jieba.cut(data.text, cut_all=True)
        for one in seg_list:
            if one != "":
                if one not in redian_dic:
                    redian_dic[one] = 1
                else:
                    redian_dic[one] += 1
        count += 1
    except Exception as e:
        count = 1
        break

res = sorted(redian_dic.items(), key=lambda d: d[1], reverse=True)
print(res)
try:
    driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[3]/div[1]/div[2]").click()
except Exception as e:
    time.sleep(5)
    driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[3]/div[1]/div[2]").click()
vedio_base_xpath = "/html/body/div[2]/div[1]/div[3]/div[3]/div[{}]/div[2]/div[1]/span[1]"
time.sleep(10)
while 1:
    try:
        data = driver.find_element_by_xpath(vedio_base_xpath.format(str(count)))
        seg_list = jieba.cut(data.text, cut_all=True)
        for one in seg_list:
            if one != "":
                if one not in vedio_dic:
                    vedio_dic[one] = 1
                else:
                    vedio_dic[one] += 1
        count += 1
    except Exception as e:
        break

res = sorted(vedio_dic.items(), key=lambda d: d[1], reverse=True)
print(res)
