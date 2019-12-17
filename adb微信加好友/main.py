#!/usr/local/bin/python
# -*- coding:utf-8 -*-

"""
 @author: valor
 @file: main.py
 @time: 2018/11/5 15:59
"""

from enum import Enum
import re
import os
import xml.etree.cElementTree as xmlParser
import xlrd
from platform import system
from enum import Enum
from os import path
import smtplib  # 发送邮件 连接邮件服务器
from email.mime.text import MIMEText  # 构建邮件格式
from xlutils.copy import copy
import time

from configparser import ConfigParser

# 读取配置文件
config_parser = ConfigParser()
config_parser.read('config.cfg', encoding="utf-8-sig")
config = config_parser['default']
phone_file_path = config['phone_file_path']
phone_excel = xlrd.open_workbook(phone_file_path)
phoe_tables = phone_excel.sheet_by_index(0)
phone_get_col = 1
phone_write_col = 2


class By(Enum):
    text = 'text'
    content = 'content-desc'
    naf = 'NAF'


def adb_path():
    """
    获取adb路径
    :return:
    """
    os = system().lower()
    _path = path.dirname(__file__)
    return _path + '/adb/' + os + '/platform-tools/'


# adb对应命令
# https://www.cnblogs.com/yoyoketang/p/8988203.html
class Adb:
    def __init__(self, port=None, device=None):
        self._port = port
        self._device = device

        self._p = '' if (port is None) else '-P ' + str(port) + ' '
        self._s = '' if (device is None) else '-s ' + str(device) + ' '

        # 指定端口 指定设备 组装adb命令
        self._baseShell = adb_path() + 'adb ' + self._p + self._s
        # 获取该文件(adbtools.py) 所在对文件夹路径
        self._basePath = os.path.dirname(__file__)

        # 缓存xml 不需要多此进行文件读取操作
        self._xml = None
        # 缓存当前查找到的nodes => type 列表 | value 字典
        self._nodes = None

        self._x = None
        self._y = None

    def printf(self):
        pass
        # print(self._port)
        # print(self._device)
        # print(self._p)
        # print(self._s)
        # print(self._baseShell)

    def adb_keyboard(self, event):
        """
        不同event对应不同指令
        :param event:
        :return:
        """
        os.system(self._baseShell + 'shell input keyevent ' + str(event))

    def adb_put_back(self):
        """
        返回 back  对应4
        :return:
        """
        self.adb_keyboard(4)

    def adb_back_to_desktop(self):
        """
        返回桌面
        :return:
        """
        self.adb_keyboard(3)

    def adb_click(self, x, y):
        """
        点击x 和y 坐标
        :param x:
        :param y:
        :return:
        """
        os.system(self._baseShell + 'shell input tap ' + str(x) + ' ' + str(y))

    def adb_input(self, text):
        """
        输入文本
        :param text:
        :return:
        """
        os.system(self._baseShell + 'shell input text ' + str(text))

    def adb_refresh(self):
        """
        刷新获取node节点
        :return:
        """
        if os.system(self._baseShell + 'shell uiautomator dump /sdcard/dump.xml'):
            pass
        if os.system(self._baseShell + 'pull /sdcard/dump.xml ' + self._basePath + '/data/dump.xml'):
            pass

    def parse_xml(self):
        """
        解析xml文件获取node数据
        :return:
        """
        self._xml = xmlParser.ElementTree(file=self._basePath + '/data/dump.xml')

    def refresh_nodes(self):
        """
        刷新节点并解析xml数据
        :return:
        """
        self.adb_refresh()
        self.parse_xml()

    def find_nodes_by_xpath(self, xpath):
        """
        通过xpath寻找节点
        :param xpath:
        :return:
        """
        # 迭代器只能循环一次 故使用self._nodes作为列表保存节点
        nodes = self._xml.iterfind(path=xpath)

        self._nodes = []
        for _node in nodes:
            # elem.attrib 为字典
            self._nodes.append(_node.attrib)
        return self._nodes

    def find_nodes(self, txt, by: By, index=None):
        _index = '' if (index is None) else '[' + str(index) + ']'
        return self.find_nodes_by_xpath(xpath='.//node[@' + by.value + '="' + txt + '"]' + _index)

    def find_nodes_by_text(self, text, index=None):
        """
        通过text寻找节点
        :param text:
        :param index:
        :return:
        """
        return self.find_nodes(text, By.text, index)

    def find_nodes_by_content(self, content, index=None):
        """
        通过content寻找节点
        :param content:
        :param index:
        :return:
        """
        return self.find_nodes(content, By.content, index)

    def get_bounds(self):
        """
        获取边界值
        :return:
        """
        _bounds = self._nodes[0]['bounds']
        pattern = re.compile(r'\d+')
        return pattern.findall(_bounds)

    def cal_coordinate(self, index=None):
        """
        计算坐标中心点
        :param index:
        :return:
        """
        if self._nodes:
            _index = 0 if (index is None) else index
            # print("nodes",self._nodes,"index",_index)
            _bounds = self._nodes[_index]['bounds']

            pattern = re.compile(r'\d+')
            _result = pattern.findall(_bounds)
            x1 = float(_result[0])
            y1 = float(_result[1])
            x2 = float(_result[2])
            y2 = float(_result[3])

            self._x = (x1 + x2) / 2
            self._y = (y1 + y2) / 2

            return self._x, self._y

    def click(self, cal_index=None):
        """
        计算中心点后点击坐标
        :param cal_index:
        :return:
        """
        x, y = self.cal_coordinate(cal_index)
        self.adb_click(x, y)

    def click_by_text(self, text, index=None):
        self.find_nodes_by_text(text, index)
        self.click(0)

    def click_by_content(self, content, index=None):
        self.find_nodes_by_content(content, index)
        self.click(0)

    def click_by_text_after_refresh(self, text, index=None):
        self.refresh_nodes()
        self.click_by_text(text, index)

    def click_by_content_after_refresh(self, content, index=None):
        self.refresh_nodes()
        self.click_by_content(content, index)


def get_keywords_data(tables, row, col):
    """
    从excel中读取数据
    :param tables:
    :param row:
    :param col:
    :return:
    """
    actual_data = tables.cell_value(row, col)
    return actual_data


def write_to_excel(file_path, row, col, value):
    """
    往excel中写入数据
    :param file_path:
    :param row:
    :param col:
    :param value:
    :return:
    """
    work_book = xlrd.open_workbook(file_path, formatting_info=False)
    write_to_work = copy(work_book)
    sheet_data = write_to_work.get_sheet(0)
    sheet_data.write(row, col, str(value))
    write_to_work.save(file_path)


class Main:
    def __init__(self, port=None, device=None):
        self._adb = Adb(port, device)

        # 用于查找失败三次时 程序暂停半小时
        self._flag = 0

        self._success = []
        self._failed = []

        self._dict = {'success': self._success, 'failed': self._failed}

        # self._json = self._file.json()
        #
        # self._file = self._json['file']
        # # 自动切换账号 微信登录 微信预留账号
        # self._account = self._json['account']
        # # 累计查找结果达到指定个数 会从内存写入到文件
        # self._dump = self._json['dump']
        # # 切换账号达到一定次数 会休眠 单位分钟
        self._sleep = 1
        # # 切换账号指定次数
        self._sleep_flag = 1

    # 输出添加结果到内存 或 文件
    def push(self, key, value):
        print("保存到文件")

    def init(self):
        pass
        # self._adb.click_by_text_after_refresh('通讯录')
        # self._adb.click_by_text_after_refresh('外部联系人')
        # self._adb.click_by_text_after_refresh('添加')
        # self._adb.click_by_text_after_refresh('微信号/手机号')

    def change_user(self):
        """
        切换微信账号
        :return:
        """
        print(' ---- 开始切换账号 ----')

        # 企业微信退回到主页面
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self._adb.adb_put_back()
        self._adb.click_by_text_after_refresh('我')

        # 回到桌面
        self._adb.adb_back_to_desktop()

        # 切换微信
        self._adb.click_by_text_after_refresh('微信')
        self._adb.click_by_text_after_refresh('我')
        self._adb.click_by_text_after_refresh('设置')
        self._adb.click_by_text_after_refresh('切换帐号')

        # 判断当前使用哪个账号
        self._adb.refresh_nodes()

        self._adb.find_nodes_by_text(self._account[0])
        left = float(self._adb.get_bounds()[0])

        self._adb.find_nodes_by_text(self._account[1])
        right = float(self._adb.get_bounds()[0])

        self._adb.find_nodes_by_text('当前使用')
        cursor = float(self._adb.get_bounds()[0])

        self._adb.find_nodes('true', By.naf)
        # 左侧用户在使用中
        if abs(cursor - left) < abs(cursor - right):
            self._adb.click(1)
        else:
            self._adb.click(0)

        # 判断是否登录成功
        while True:
            self._adb.refresh_nodes()
            if self._adb.find_nodes_by_text('通讯录'):
                break
            time.sleep(2)

        # 回到桌面打开企业微信
        self._adb.adb_back_to_desktop()
        self._adb.click_by_text_after_refresh('企业微信')
        self._adb.click_by_text_after_refresh('设置')
        self._adb.click_by_text_after_refresh('退出登录')
        self._adb.click_by_text_after_refresh('退出当前帐号')
        self._adb.click_by_text_after_refresh('确定')
        self._adb.click_by_text_after_refresh('微信登录')

        # 判断是否登录成功
        while True:
            self._adb.refresh_nodes()
            if self._adb.find_nodes_by_text('进入企业 '):
                break
            time.sleep(2)
        self._adb.click(0)

        while True:
            self._adb.refresh_nodes()
            if self._adb.find_nodes_by_text('通讯录'):
                break
            time.sleep(2)

    def add_friends(self, phone):
        print('===== 开始查找 ===== ' + phone + ' =====')
        self._adb.click_by_text_after_refresh('微信号/手机号')

        # 输入号码
        self._adb.adb_input(phone)
        # 点击搜索
        self._adb.click_by_text_after_refresh('搜索:' + phone)
        print('  ==> 点击搜索 ==>  ')

        self._adb.refresh_nodes()
        if self._adb.find_nodes_by_text('查找失败'):
            print('  <== 查找失败 <==  ')
            self.push('failed', phone + '查找失败')
            self._adb.adb_put_back()

            print(' ---- 计算切换账号次数 ----')
            self._flag += 1
            if int(self._sleep_flag) == self._flag:
                print(' ---- 休眠半小时 ----')
                time.sleep(int(self._sleep) * 60)
                self._flag = 0
            else:
                print(' ---- 开始切换账号 ----')
                self.init()

        # 查找成功
        elif self._adb.find_nodes_by_text('添加到通讯录'):
            # self._adb.click(0)
            self._adb.click_by_text_after_refresh('发送')

            self._adb.refresh_nodes()
            if self._adb.find_nodes_by_text('发送添加邀请'):
                print('  <== 发送失败 <==  ')
                self.push('failed', phone + '发送失败')
                self._adb.adb_put_back()
                self._adb.adb_put_back()
            else:
                print(' !! <== 发送成功 <==  ')
                self.push('success', phone + '发送成功')
                self._adb.adb_put_back()

        elif self._adb.find_nodes_by_text('发消息'):
            print('  <== 已经是好友 无需再次添加 <==  ')
            self.push('failed', phone + '已经是好友')
            self._adb.adb_put_back()

        elif self._adb.find_nodes_by_text('同时拥有微信和企业微信'):
            print('  <== 同时拥有微信和企业微信 <==  ')
            self.push('failed', phone + '同时拥有微信和企业微信')
            self._adb.adb_put_back()

        elif self._adb.find_nodes_by_text('该用户不存在') or self._adb.find_nodes_by_text('被搜帐号状态异常，无法显示'):
            print('  <== 该用户不存在 或 帐号异常 <==  ')
            self.push('failed', phone + '该用户不存在 或 帐号异常')
            self._adb.adb_put_back()

        # 清空已输入的字符
        self._adb.refresh_nodes()
        if self._adb.find_nodes('true', By.naf):
            self._adb.click(1)

    def main(self):
        self.init()
        phone_datas = [get_keywords_data(phoe_tables, i, phone_get_col) for i in
                       range(1, phoe_tables.nrows)]
        for phone in phone_datas:
            self.add_friends(phone)


if __name__ == '__main__':
    fun = Main()
    fun.main()
