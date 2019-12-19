#!/usr/local/bin/python
# -*- coding:utf-8 -*-

"""
 @author: valor
 @file: main.py
 @time: 2018/11/5 15:59
"""

import traceback
import os
import xml.etree.cElementTree as xmlParser
import xlrd
from platform import system
from enum import Enum
from os import path
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
phone_get_col = 1  # 读取手机号的列
phone_write_col = 2  # 写入手机号的列
wait_time = 1  # 各个操作等待间隔
phone_can_write_index = 1  # 从哪一行开始记录手机号


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


def screenshot_prepare(pagename, firstActivty):
    """
    打开app
    """
    try:
        displayPowerState = os.popen(
            "adb shell dumpsys power | grep 'Display Power: state=' | awk -F '=' '{print $2}'").read().strip()
        # print(displayPowerState)
        if displayPowerState == 'OFF':
            print("唤醒屏幕")
            os.system('adb shell input keyevent 26')
        else:
            print("屏幕已开启不需要唤醒")
        isStatusBarKeyguard = os.popen(
            "adb shell dumpsys window policy|grep isStatusBarKeyguard | awk -F '=' ' {print $3}'").read().strip('\n')
        # print(isStatusBarKeyguard)
        if isStatusBarKeyguard == 'true':
            time.sleep(2)
            print("解锁屏保")
            # 左右滑动才好解锁,并且延迟100ms启动
            os.system('adb shell input swipe 200 400 800 400 100')
            # time.sleep(1)
            # print("输入密码")
            # os.system('adb shell input text 95729')
        else:
            print("屏幕已解锁不需要再次解锁")
        time.sleep(1)

        cmd = "adb shell am start -W -n " + pagename + firstActivty
        content = os.popen(cmd)

        mFocusedActivity = os.popen(
            "adb shell dumpsys activity | grep 'mFocusedActivity' | awk '{print $4}' | awk -F '/' '{print $1}'").read().strip(
            '\n')
        if mFocusedActivity == 'com.eg.android.AlipayGphone':
            print("APP已启动，停止APP，等待重新启动")
            os.system('adb shell am force-stop com.eg.android.AlipayGphone')
        time.sleep(1)
        print("启动app")
        os.system('adb shell am start -n com.eg.android.AlipayGphone/com.eg.android.AlipayGphone.AlipayLogin activity')
    except Exception:
        print("screenshot_prepare error")
        traceback.print_exc()
        exit(-1)

# adb对应命令
# https://www.cnblogs.com/yoyoketang/p/8988203.html
class Adb:
    def __init__(self, port=None, device=None):
        self._port = port  # 端口
        self._device = device  # 设备号
        self._p = '' if (port is None) else '-P ' + str(port) + ' '
        self._s = '' if (device is None) else '-s ' + str(device) + ' '
        self._baseShell = adb_path() + 'adb ' + self._p + self._s  # 指定端口 指定设备 组装adb命令
        self._basePath = os.path.dirname(__file__)  # 获取该文件(adbtools.py) 所在对文件夹路径
        self._nodes = None  # 缓存当前查找到的nodes => type 列表 | value 字典
        self._x = None
        self._y = None

    def adb_keyboard(self, event):
        """
        不同event对应不同指令
        :param event:
        :return:
        """
        os.system(self._baseShell + 'shell input keyevent ' + str(event))

    def check_screen(self):
        """
        判断屏幕状态 亮为True
        :return:
        """
        displayPowerState = os.popen(
            "adb shell dumpsys window policy | findstr mScreenOnFully ").read().strip()  # 读出来这种 mAwake=truemScreenOnEarly=true mScreenOnFully=true  字节类型
        state = str(displayPowerState).split(" ")[1].split("=")[1]
        if state == 'true':
            return True
        return False

    def wake_up_the_screen(self):
        """
        唤醒屏幕  26  如果已唤醒则跳过
        :return:
        """
        if not self.check_screen():
            self.adb_keyboard(26)

    def check_screen_lock(self):
        """
        判断屏幕是否锁屏 是True
        :return:
        """
        displayPowerState = os.popen(
            'adb shell dumpsys window policy |find "isStatusBarKeyguard"').read().strip()  # 读出来这种 mAwake=truemScreenOnEarly=true mScreenOnFully=true  字节类型
        state = str(displayPowerState).split(" ")[-1].split("=")[-1]
        if state == 'true':
            return True
        return False

    def unlock(self):
        """
        解锁  82 已解锁则跳过
        :return:
        """
        if self.check_screen_lock():
            self.adb_keyboard(82)

    def start_wechat(self):
        """
        启动微信
        :return:
        """
        os.system(self._baseShell + "shell am start com.tencent.mm/com.tencent.mm.ui.LauncherUI")

    def check_wechat_is_start(self):
        """
        判断微信是否启动
        :return:
        """
        return self.find_node_by_text("微信")

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
        os.system(self._baseShell + 'shell uiautomator dump /sdcard/dump.xml')
        os.system(self._baseShell + 'pull /sdcard/dump.xml ' + self._basePath + '/data/dump.xml')

    def generate_nodes(self):
        """
        解析xml文件生成node数据
        :return:
        """
        xml = xmlParser.ElementTree(file=self._basePath + '/data/dump.xml')
        nodes = xml.findall(path=".//node")  # 全部node节点
        tem_node = []
        for _node in nodes:
            # print(_node.attrib)
            # elem.attrib 为字典
            tem_node.append(_node.attrib)
        self._nodes = tem_node

    def find_nodes_by_class_name(self, class_name):
        """
        获取class为class_name的所有元素的坐标列表
        :param txt:
        :return:
        """
        self.adb_refresh()
        self.generate_nodes()
        results = []
        for node in self._nodes:
            if node['class'] == class_name:
                results.append(node['bounds'])
        return results

    def find_node_by_class_name(self, class_name, index=0):
        """
        找单个节点
        :param txt:
        :param by:
        :param index:
        :return:
        """

        results = self.find_nodes_by_class_name(class_name)
        if results:
            if index > len(results):
                return results[0]
            return results[index]
        return None

    def find_nodes_by_resource_id(self, id):
        """
        获取resource-id为id的所有元素的坐标列表
        :param txt:
        :return:
        """
        self.adb_refresh()
        self.generate_nodes()
        results = []
        for node in self._nodes:
            if node['resource-id'] == id:
                results.append(node['bounds'])

        if len(results) > 0:
            return results
        return None

    def find_node_by_resource_id(self, id, index=0):
        """
        :param txt:
        :param by:
        :param index:
        :return:
        """
        results = self.find_nodes_by_resource_id(id)
        if results:
            if index > len(results):
                return results[0]
            return results[index]
        return None

    def find_nodes_by_text(self, txt):
        """
        获取text=txt的所有元素的坐标列表
        :param txt:
        :return:
        """
        self.adb_refresh()
        self.generate_nodes()
        results = []
        for node in self._nodes:
            if node['text'] == txt:
                results.append(node['bounds'])

        return results

    def find_node_by_text(self, txt, index=0):
        """
        返回找到的第index个节点的坐标 'bounds': '[0,550][1080,744]'}  左上角x y 右下角x y
        找不到或者超出索引返回第一个
        :param txt:
        :param by:
        :param index:
        :return:
        """

        results = self.find_nodes_by_text(txt)
        if results:
            if index > len(results):
                return results[0]
            return results[index]
        return None

    def cal_coordinate(self, bounds):
        """
        计算坐标中心点
        :param index:
        :return:
        """
        # [436,260][731,322] 字符串形式
        try:
            bounds = bounds.replace("[", "").replace("]", ',').split(",")
            x1 = float(bounds[0])
            y1 = float(bounds[1])
            x2 = float(bounds[2])
            y2 = float(bounds[3])
            self._x = (x1 + x2) / 2
            self._y = (y1 + y2) / 2

            return self._x, self._y
        except Exception as e:
            print("没有检测到该内容")

    def click(self, x, y):
        """
        点击坐标
        :param cal_index:
        :return:
        """
        self.adb_click(x, y)

    def click_add_friend(self):
        """
        点击添加好友  共两个操作 1，点击+号按钮 2，点击“添加朋友”
        :return:
        """
        self.click_by_id_after_refresh("com.tencent.mm:id/rb")
        self.click_by_text_after_refresh("添加朋友")

    def click_wechat_and_friend(self):
        """
        点击那两个 微信号/手机号
        :return:
        """
        bounds1 = self.find_node_by_resource_id("com.tencent.mm:id/dlc")
        self.click_use_bounds(bounds1)
        bounds2 = self.find_node_by_resource_id("com.tencent.mm:id/c4j")
        self.click_use_bounds(bounds2)

    def click_use_bounds(self, bounds):
        x, y = self.cal_coordinate(bounds)
        self.click(x,y)

    def click_by_text(self, text, index=0):
        """
        通过text点击
        :param text:
        :param index:
        :return:
        """
        bounds = self.find_node_by_text(text, index)
        x, y = self.cal_coordinate(bounds)
        self.click(x, y)

    def click_by_text_after_refresh(self, text, index=0):
        """
        封装之前的代码 刷新节点后通过text点击
        :param text:
        :return:
        """
        bounds = self.find_node_by_text(text, index)
        x, y = self.cal_coordinate(bounds)
        self.click(x, y)

    def click_by_id_after_refresh(self, id, index=0):
        """
        封装之前的代码 刷新节点后通过id点击
        :param text:
        :return:
        """
        self.adb_refresh()
        self.generate_nodes()
        bounds = self.find_node_by_resource_id(id, index)
        x, y = self.cal_coordinate(bounds)
        self.click(x, y)

    def click_by_class_name_after_refresh(self, class_name, index=0):
        """
        封装之前的代码 刷新节点后通过class_name点击
        :param text:
        :return:
        """

        bounds = self.find_node_by_class_name(class_name, index)
        x, y = self.cal_coordinate(bounds)
        self.click(x, y)


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
        切换微信账号  暂未完成
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

    def clean_phone(self):
        """
        清空手机号
        :return:
        """
        if self._adb.find_node_by_resource_id('com.tencent.mm:id/m3'):
            self._adb.click_by_id_after_refresh("com.tencent.mm:id/m3")
            print("清空成功")
            return True
        return False

    def add_friends(self, phone):
        # 输入号码
        self._adb.adb_input(phone)
        # 点击搜索

        search_res = "搜索:" + phone
        self._adb.click_by_text_after_refresh(search_res)
        print('  ==> 点击搜索 ==>  ')

        if self._adb.find_node_by_text('查找失败'):
            print('  <== 查找失败 <==  ')
            write_to_excel(phoe_tables, phone_can_write_index, phone_write_col, "查找失败")
            self._adb.adb_put_back()

        # 查找成功
        elif self._adb.find_node_by_text('添加到通讯录'):

            # self._adb.click(0)
            self._adb.click_by_text_after_refresh('添加到通讯录')

            if not self._adb.find_node_by_text('发送添加朋友申请'):
                print('  <== 发送失败 <==  ')
                write_to_excel(phoe_tables, phone_can_write_index, phone_write_col, "发送失败")

            else:
                self._adb.click_by_text_after_refresh("发送")

                print(' !! <== 发送成功 <==  ')
                write_to_excel(phoe_tables, phone_can_write_index, phone_write_col, "发送成功")
                time.sleep(2)
                self._adb.adb_put_back()
                if self._adb.find_node_by_text('添加到通讯录'):
                    print("操作可能太频繁被限制,建议换号或者等会再试")
                    self._adb.adb_put_back()



        elif self._adb.find_node_by_text('发消息'):
            print('  <== 已经是好友 无需再次添加 <==  ')
            write_to_excel(phoe_tables, phone_can_write_index, phone_write_col, "已经是好友")
            self._adb.adb_put_back()

        # elif self._adb.find_node_by_text('同时拥有微信和企业微信'):
        #     print('  <== 同时拥有微信和企业微信 <==  ')
        #     self.push('failed', phone + '同时拥有微信和企业微信')
        #     self._adb.adb_put_back()

        elif self._adb.find_node_by_text('该用户不存在') or self._adb.find_node_by_text('被搜帐号状态异常，无法显示'):
            print('  <== 该用户不存在 或 帐号异常 <==  ')
            write_to_excel(phoe_tables, phone_can_write_index, phone_write_col, "已经是好友")

        # 清空已输入的字符
        self.clean_phone()


    def main(self):
        #读取手机号数据
        phone_datas = [get_keywords_data(phoe_tables, i, phone_get_col) for i in
                       range(1, phoe_tables.nrows)]
        for phone in phone_datas:
            self.add_friends(phone)

    def test(self):

        # 唤醒屏幕
        self._adb.wake_up_the_screen()
        # 解锁 此处只能滑动解锁
        self._adb.unlock()
        # 启动微信
        self._adb.start_wechat()
        # 判断微信是否启动
        self._adb.check_wechat_is_start()
        # 添加好友
        self._adb.click_add_friend()
        # 点击那两个 微信号/手机号
        self._adb.click_wechat_and_friend()
        # 添加好友
        phone_datas = [get_keywords_data(phoe_tables, i, phone_get_col) for i in
                       range(1, phoe_tables.nrows)]
        for phone in phone_datas:
            self.add_friends(phone)


if __name__ == '__main__':
    fun = Main()
    # fun.main()
    fun.test()
