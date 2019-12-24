import time
import jieba
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('window-size=1200,1100')
driver = webdriver.Chrome(chrome_options=chrome_options,
                          executable_path=r'C:\Users\lenovo\PycharmProjects\Spider\chromedriver.exe')

url = "https://news.sina.com.cn/world/"
driver.get(url)

titles = driver.find_elements_by_css_selector(".news-item > h2")
for one in titles:
    print(one.text)
