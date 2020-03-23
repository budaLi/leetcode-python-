# @Time    : 2020/3/18 21:01
# @Author  : Libuda
# @FileName: main.py
# @Software: PyCharm
from selenium import webdriver
import csv
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument(
    'user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')
# chrome_options.add_argument('--no-sandbox')  # 这个配置很重要
txt_name = "res.csv"
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="chromedriver.exe")
driver.get("https://developer.aliyun.com/my")
y = input("请手动登录并翻页至文章页,输入y进行爬取:")

if y:
    while 1:
        titles = driver.find_elements_by_class_name("question-title .title-text")
        times = driver.find_elements_by_class_name(".ques-info .time")
        views = driver.find_elements_by_class_name(".ques-info .browsing-volume")
        for index in range(len(titles)):
            with open(txt_name, 'a', newline='') as f:
                writer = csv.writer(f)
                row_item = ["" for _ in range(3)]
                row_item[0] = titles[index]
                row_item[1] = times[index]
                row_item[2] = views[index]
        next = driver.find_element_by_class_name(".next-btn")
        if next:
            next.click()
        else:
            break
