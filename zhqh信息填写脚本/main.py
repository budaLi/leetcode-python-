# @Time    : 2020/3/31 16:49
# @Author  : Libuda
# @FileName: main.py
# @Software: PyCharm

from selenium import webdriver
import time
from configparser import ConfigParser

config_parser = ConfigParser()
config_parser.read('config.cfg', encoding="utf-8-sig")
config = config_parser['default']

name = config['姓名']
idcard_z = config['身份证正面图']
idcard_f = config['身份证反面图']
signuture = config['手写签名']
idcard_num = config['身份证']
address = config['联系地址']
code = config['邮政编码']
phone = config['联系电话']
email = config["邮箱"]
zhiye = config['职业']
xueli = config['学历']
yingyebu = config['开户营业部']
yinghang = config['银行']
yinghangka = config['银行卡账号']
wangdian = config['银行网点']
question_answer = config['question_answer']

iedriver = webdriver.Ie("D:\PycharmProjects\leetcode-python-\zhqh信息填写脚本\IEDriverServer.exe")


def logger(msg):
    """
    日志信息
    """
    now = time.ctime()
    print("[%s] %s" % (now, msg))


def main():
    iedriver.get("https://zhqh.cfmmc.com/")

    login_confirm = input("请输入您的手机号，图片验证码及短信验证码，回车键进行下一步：")

    if login_confirm:
        pass

    logger("上传您的身份证及手写签名中，请稍后")
    # 身份证正面
    iedriver.find_element_by_class_name("").send_keys(idcard_z)
    # 身份证背面
    iedriver.find_element_by_class_name("").send_keys(idcard_f)
    # 手写签名
    iedriver.find_element_by_class_name("").send_keys(signuture)
    # 确认接收协议
    iedriver.find_element_by_class_name("").click()

    next_confirm = input("回车进行下一步")

    if next_confirm:
        pass

    # 点击下一步
    iedriver.find_element_by_class_name("").click()

    # 资料报审页面
    # 客户姓名
    iedriver.find_element_by_class_name("").send_keys(name)
    # 身份证号
    iedriver.find_element_by_class_name("").send_keys(idcard_num)
    # 联系地址
    iedriver.find_element_by_class_name("").send_keys(address)
    # 邮政编码
    iedriver.find_element_by_class_name("").send_keys(code)
    # 联系电话
    iedriver.find_element_by_class_name("").send_keys(phone)
    # 邮箱
    iedriver.find_element_by_class_name("").send_keys(email)
    # 职业
    iedriver.find_element_by_class_name("").send_keys(zhiye)
    # 学历
    iedriver.find_element_by_class_name("").send_keys(xueli)
    # 开户营业部
    iedriver.find_element_by_class_name("").send_keys(yingyebu)

    next_confirm = input("请确认资料报审信息,回车键继续")

    if next_confirm:
        pass

    # 下一步
    iedriver.find_element_by_class_name("").click()

    # 指定结算银行

    # 银行卡账号
    iedriver.find_element_by_class_name("").click(idcard_num)

    # 银行网点

    # 上传银行卡照片
    iedriver.find_element_by_class_name("").send_keys()

    next_confirm = input("上传银行卡照片，回车继续")
    if next_confirm:
        pass

    # 选择题填写

    next_confirm = input("确认选择题选择完毕，回车继续")
    if next_confirm:
        pass

    # 下一步


if __name__ == '__main__':
    main()
