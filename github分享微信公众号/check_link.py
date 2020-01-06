# @Time    : 2020/1/6 17:45
# @Author  : Libuda
# @FileName: check_link.py
# @Software: PyCharm


from selenium import webdriver
import time
import datetime
from configparser import ConfigParser

config_parser = ConfigParser()
config_parser.read('config.cfg', encoding="utf-8-sig")
config = config_parser['default']

driver = webdriver.Chrome(config['executable_path'])

file_path = r"C:\Users\lenovo\PycharmProjects\leetcode-python-\github分享微信公众号\link"
res_path = r"C:\Users\lenovo\PycharmProjects\leetcode-python-\github分享微信公众号\new"


def check_link():
    """
    检测链接
    :return:
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = f.readlines()
        for one in data:
            one = one.strip().split(" ")
            if one != [""]:
                number, link, code = one
                driver.get(link.strip())
                try:
                    text = driver.find_element_by_css_selector(".error-img")
                except Exception:
                    tem = number + " " + link + " " + code
                    print(tem)


def change_number():
    """
    更改编号
    :return:
    """
    res = []
    with open(file_path, "r", encoding="utf-8") as f:
        data = f.readlines()
        for index, one in enumerate(data):
            one = one.strip().split(" ")
            print(one)
            if len(one) >= 3:
                number, link, code = "".join(one[:-2]), one[-2], one[-1]
            else:
                number, link, code = one
            number = "【{}】".format(index) + number.split("】")[-1]
            res.append(number + " " + link + " " + code)
    with open(res_path, "w") as f:
        for one in res:
            f.write(one + "\n")
            f.write("\n")


if __name__ == '__main__':
    change_number()
