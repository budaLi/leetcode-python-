#!/usr/local/bin/python
# -*- coding:utf-8 -*-

"""
 @author: libuda
 @file: 远程服务器文件监控.py
 @time: 2019/12/5 15:59
"""
import traceback
import os
import xml.etree.cElementTree as xmlParser
import xlrd
from platform import system
import subprocess
from os import path
import time
from configparser import ConfigParser
import pandas as pd
from pandas import DataFrame
from copy import deepcopy

# 读取配置文件
config_parser = ConfigParser()
config_parser.read('config.cfg', encoding="utf-8-sig")
config = config_parser['default']
phone_file_path = config['phone_file_path']
phone_excel = xlrd.open_workbook(phone_file_path)
phoe_tables = phone_excel.sheet_by_index(0)
phone_get_col = 1  # 读取手机号的列
phone_write_col = 2  # 写入手机号的列
wait_time = 20  # 等待间隔
phone_can_write_index = 1  # 从哪一行开始记录手机号
all_sleep = 1  # 各个操作等待时间


def logger(msg):
    """
    日志信息
    """
    now = time.ctime()
    print("[%s] %s" % (now, msg))


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
            "adb shell dumpsys power | grep 'Display Power: state=' | awk -F '=' '{logger $2}'").read().strip()
        # logger(displayPowerState)
        if displayPowerState == 'OFF':
            logger("唤醒屏幕")
            os.system('adb shell input keyevent 26')
        else:
            logger("屏幕已开启不需要唤醒")
        isStatusBarKeyguard = os.popen(
            "adb shell dumpsys window policy|grep isStatusBarKeyguard | awk -F '=' ' {logger $3}'").read().strip('\n')
        # logger(isStatusBarKeyguard)
        if isStatusBarKeyguard == 'true':
            time.sleep(2)
            logger("解锁屏保")
            # 左右滑动才好解锁,并且延迟100ms启动
            os.system('adb shell input swipe 200 400 800 400 100')
            # time.sleep(1)
            # logger("输入密码")
            # os.system('adb shell input text 95729')
        else:
            logger("屏幕已解锁不需要再次解锁")
        time.sleep(1)

        cmd = "adb shell am start -W -n " + pagename + firstActivty
        content = os.popen(cmd)

        mFocusedActivity = os.popen(
            "adb shell dumpsys activity | grep 'mFocusedActivity' | awk '{logger $4}' | awk -F '/' '{logger $1}'").read().strip(
            '\n')
        if mFocusedActivity == 'com.eg.android.AlipayGphone':
            logger("APP已启动，停止APP，等待重新启动")
            os.system('adb shell am force-stop com.eg.android.AlipayGphone')
        time.sleep(1)
        logger("启动app")
        os.system('adb shell am start -n com.eg.android.AlipayGphone/com.eg.android.AlipayGphone.AlipayLogin activity')
    except Exception:
        logger("screenshot_prepare error")
        traceback.logger_exc()
        exit(-1)


# adb对应命令
# https://www.cnblogs.com/yoyoketang/p/8988203.html
class Adb:
    def __init__(self, port=None, device=None):
        self._port = port  # 端口
        self._device = device  # 设备号
        self._p = '' if (port is None) else '-P ' + str(port) + ' '
        self._s = '' if (device is None) else '-s ' + str(device) + ' '
        self._basePath = os.path.dirname(__file__)  # 获取该文件(adbtools.py) 所在对文件夹路径
        self._baseShell = adb_path() + 'adb ' + self._p + self._s  # 指定端口 指定设备 组装adb命令
        self._nodes = None  # 缓存当前查找到的nodes => type 列表 | value 字典
        self._x = None
        self._y = None

    def get_phone_resolution(self):
        """
        获取设备分辨率
        :return:
        """
        displayPowerState = os.popen(
            "adb shell wm size").read().strip()  # Physical size: 1080x2244
        state = str(displayPowerState).split(" ")[-1]
        width, heidht = state.strip().split("x")
        return int(width), int(heidht)

    def get_center(self):
        """
        获取设备中心点
        :return:
        """
        width, height = self.get_phone_resolution()
        return width / 2, height / 2

    def swipe(self, start=None, end=None):
        """
        滑动屏幕 默认从屏幕底部往上滑
        :param start:
        :param end:
        :return:
        """
        if start is None:
            start = self.get_center()
        x1, y1 = start
        if end is None:
            end = x1, y1 - int(y1 / 2)
        x2, y2 = end
        cmd = self._baseShell + "shell input swipe " + str(x1) + " " + str(y1) + " " + str(x2) + " " + str(y2)
        os.system(cmd)

    def show_current_pk(self):
        """
        展示当前所在app的包名
        :return:
        """
        displayPowerState = os.popen(
            "adb shell dumpsys  window windows |findstr -i current").read().strip()  # 读出来这种 mAwake=truemScreenOnEarly=true mScreenOnFully=true  字节类型
        state = str(displayPowerState).split(" ")[-1]
        return state

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
        # logger(self._basePath)

        # os.system(self._baseShell+"shell dumpsys window policy | findstr mScreenOnFully")

        displayPowerState = os.popen(
            " bash shell dumpsys window policy | findstr mScreenOnFully ").read().strip()  # 读出来这种 mAwake=truemScreenOnEarly=true mScreenOnFully=true  字节类型
        # logger("134",displayPowerState)
        state = str(displayPowerState).split(" ")[1].split("=")[1]
        if state == 'true':
            return True
        return False

    def wake_up_the_screen(self):
        """
        唤醒屏幕  26  如果已唤醒则跳过
        :return:
        """
        # if not self.check_screen():
        self.adb_keyboard(26)

    def check_screen_lock(self):
        """
        判断屏幕是否锁屏 是True
        :return:
        """
        displayPowerState = os.popen(
            self._baseShell + 'shell dumpsys window policy |findstr isStatusBarKeyguard').read().strip()  # 读出来这种 mAwake=truemScreenOnEarly=true mScreenOnFully=true  字节类型
        state = str(displayPowerState).split(" ")[-1].split("=")[-1]
        if state == 'true':
            return True
        return False

    def return_home(self):
        """
        返回桌面
        :return:
        """
        self.adb_keyboard(3)

    def unlock(self):
        """
        解锁  82 已解锁则跳过
        :return:
        """
        # if self.check_screen_lock():
        # self.adb_keyboard(82)
        self.swipe([500, 500], [500, 1500])
        logger('解锁中')

    def start_wechat(self):
        """
        启动微信
        :return:
        """
        try:
            os.system(self._baseShell + "shell am start com.tencent.mm/com.tencent.mm.ui.LauncherUI")
        except Exception:
            logger("微信无法启动")

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

    def exit(self):
        # 退出微信
        self.adb_put_back()
        self.adb_put_back()
        self.adb_put_back()
        self.adb_put_back()
        self.adb_put_back()

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
        cmd1 = self._baseShell + 'shell uiautomator dump /sdcard/dump.xml'
        cmd2 = self._baseShell + 'pull /sdcard/dump.xml ' + self._basePath + '/data/dump.xml'

        os.system(cmd1)
        os.system(cmd2)

    def generate_nodes(self):
        """
        解析xml文件生成node数据
        :return:
        """
        # logger("file_path",self._basePath + '/data/dump.xml')
        xml = xmlParser.ElementTree(file=self._basePath + '/data/dump.xml')
        nodes = xml.findall(path=".//node")  # 全部node节点
        tem_node = []
        for _node in nodes:
            # logger(_node.attrib)
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
            logger("没有检测到该内容")

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
        try:
            self.click_by_id_after_refresh("com.tencent.mm:id/rb")
        except Exception:
            pass
        try:
            self.click_by_text_after_refresh("添加朋友")
        except Exception:
            pass

    def click_wechat_and_friend(self):
        """
        点击那两个 微信号/手机号
        :return:
        """
        try:
            bounds1 = self.find_node_by_resource_id("com.tencent.mm:id/dlc")
            self.click_use_bounds(bounds1)
            bounds2 = self.find_node_by_resource_id("com.tencent.mm:id/c4j")
            self.click_use_bounds(bounds2)
        except Exception:
            pass

    def click_use_bounds(self, bounds):
        x, y = self.cal_coordinate(bounds)
        self.click(x, y)

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

class Main:
    def __init__(self, port=None, device=None):
        self._adb = Adb(port, device)

        # 用于查找失败三次时 程序暂停半小时
        self._flag = 0

        self._success = []
        self._failed = []

        self._dict = {'success': self._success, 'failed': self._failed}
        self._sleep = 1
        # # 切换账号指定次数
        self._sleep_flag = 1

    # 输出添加结果到内存 或 文件
    def push(self, key, value):
        logger("保存到文件")

    def init(self):
        pass
        # self._adb.click_by_text_after_refresh('通讯录')
        # self._adb.click_by_text_after_refresh('外部联系人')
        # self._adb.click_by_text_after_refresh('添加')
        # self._adb.click_by_text_after_refresh('微信号/手机号')

    def clean_phone(self):
        """
        清空手机号
        :return:
        """
        if self._adb.find_node_by_resource_id('com.tencent.mm:id/m3'):
            self._adb.click_by_id_after_refresh("com.tencent.mm:id/m3")
            logger("清空成功")
            return True
        return False

    def add_friends_for_main(self, phone):
        try:
            self._adb.start_wechat()
            logger("启动微信")
            time.sleep(all_sleep)

            self._adb.click_add_friend()
            logger("点击加号")
            time.sleep(2)

            self._adb.click_wechat_and_friend()
            logger("点击那两个 微信号/手机号")
            time.sleep(all_sleep)

            phone = str(int(phone))
            logger("当前手机号：{}".format(phone))
            self._adb.adb_input(phone)
            # 点击搜索
            search_res = "搜索:" + phone
            self._adb.click_by_text_after_refresh(search_res)
            logger('  ==> 点击搜索 ==>  ')

            # 不存在
            if self._adb.find_node_by_text('该用户不存在') or self._adb.find_node_by_text('被搜帐号状态异常，无法显示'):
                logger('  <== 该用户不存在 或 帐号异常 <==  ')
                self._adb.exit()
                return "用户不存在"

            # 查找成功
            elif self._adb.find_node_by_text('添加到通讯录'):

                # self._adb.click(0)
                self._adb.click_by_text_after_refresh('添加到通讯录')

                if self._adb.find_node_by_text('发消息'):
                    logger('  <==  发送成功  <==  ')
                    self._adb.adb_put_back()
                else:
                    self._adb.click_by_text_after_refresh("发送")

                    logger(' !! <== 发送成功 <==  ')
                    time.sleep(3)
                    if self._adb.find_node_by_text('添加到通讯录'):
                        logger("操作可能太频繁被限制,建议换号或者等会再试")
                        self._adb.adb_put_back()
                self._adb.exit()
                return "发送成功"

            # 已经是好友
            elif self._adb.find_node_by_text('发消息'):
                logger('  <== 已经是好友 无需再次添加 <==  ')
                self._adb.exit()
                return "已经是好友"

                #
                # # 清空已输入的字符
                # self.clean_phone()


        except Exception as e:
            logger("出现异常:{}，将重新进行本次加好友".format(e))
            self._adb.exit()
            self._adb.start_wechat()
            return self.add_friends_for_main(phone)

    def main(self):
        """
        间断时间较长
        :return:
        """
        df = pd.read_excel(phone_file_path)

        test_data = []
        for i in df.index.values:  # 获取行号的索引，并对其进行遍历：
            # 根据i来获取每一行指定的数据 并利用to_dict转成字典
            row_data = df.loc[i, ['date', 'phone']].to_dict()
            test_data.append(row_data)
        logger("Excel获取到的数据是：{0}".format(test_data))
        tem = deepcopy(test_data)
        for index, data in enumerate(test_data):
            writer = pd.ExcelWriter(phone_file_path, cell_overwrite_ok=True)
            dataframe = DataFrame()
            phone = str(int(data['phone']))
            logger("*" * 50)
            logger("手机号总数：{}，当前已添加至第{}个号码:{}".format(len(test_data), index + 1, phone))
            res = self.add_friends_for_main(phone)
            tem.pop()
            if len(tem) <= 0:
                tem = [{"date": "", "phone": ""}]

            dataframe = dataframe.append(DataFrame(tem))
            dataframe.to_excel(writer, index=0)
            writer.save()

            logger("当前剩余手机号：{}个".format(len(tem)))
            logger("*" * 50)
            if res == "发送成功":
                time.sleep(wait_time)
        y = input("{}个电话号码已加完，是否关闭程序".format(len(test_data)))
        if y:
            pass


if __name__ == '__main__':
    fun = Main()
    logger("*" * 50)
    logger("请确保屏幕已经在微信界面")
    logger("*" * 50)
    fun.main()
