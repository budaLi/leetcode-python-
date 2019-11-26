# @Time    : 2019/11/26 20:39
# @Author  : Libuda
# @FileName: spider.py
# @Software: PyCharm
import pandas
from selenium import webdriver

driver = webdriver.Chrome(r'C:\Users\lenovo\PycharmProjects\Spider\chromedriver.exe')
df = pandas.DataFrame()
file_path = r"C:\Users\lenovo\PycharmProjects\leetcode-python-\樊登读书脚本\link.xlsx"

data = pandas.read_excel(file_path)
res = ["11", '122', '222']
data['res'] = res
# for link in data['二维码']:
#     print(link)
#     driver.get(link)
#     try:
#         text = driver.find_element_by_xpath("/html/body/div[1]/div[1]/p[1]")
#         if text.text=="开卡失败":
#             res.append("已使用")
#         else:
#             print(text.text)
#             continue
#     except Exception as e :
#         print(e)
#     try:
#         text = driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/p')
#         if text.text=="欢迎加入樊登读书，即刻获得":
#             res.append("正在领取")
#         else:
#             print(text.text)
#             continue
#     except Exception as e :
#         print(e)
#     print(res)
data['res'] = res
