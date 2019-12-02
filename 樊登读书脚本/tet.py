# @Time    : 2019/12/2 17:00
# @Author  : Libuda
# @FileName: tet.py
# @Software: PyCharm

import xlrd
from xlutils.copy import copy
from selenium import webdriver
import time

wait_time = 3  # 各个阶段等待时间

driver = webdriver.Chrome(r'C:\Users\lenovo\PycharmProjects\Spider\chromedriver.exe')

driver.get("https://www.baidu.com")
windows = driver.current_window_handle

js = 'window.open("https://www.sogou.com");'
driver.execute_script(js)
for wins in driver.window_handles:
    if wins != windows:
        driver.switch_to.window(wins)
        driver.get("http://weibo.com")

time.sleep(5)
driver.close()

driver.switch_to.window(windows)
