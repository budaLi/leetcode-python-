# @Time    : 2020/3/24 16:42
# @Author  : Libuda
# @FileName: register_3_24.py
# @Software: PyCharm

import requests
import xlrd
from xlutils.copy import copy
import time
from 远程文件传输.config import get_config
import pandas as pd
from pandas import DataFrame
from copy import deepcopy

config = get_config()

user_list = ['1364826576@qq.com']

wait_time = 0.5  # 各个阶段等待时间
time_jiange = 30  # 时间间隔 隔多长时间执行脚本一次

ding_num = 5  # 链接条数报警阈值

link_file_path = config['link_file_path']

link_ecel = xlrd.open_workbook(link_file_path)
link_tables = link_ecel.sheet_by_index(0)
link_get_col = 2
link_write_col = 3

link_can_use_index = int(config['start_link_index'])
totle_break_set = set()


def logger(msg):
    """
    日志信息
    """
    now = time.ctime()
    print("[%s] %s" % (now, msg))


def get_keywords_data(tables, row, col):
    actual_data = tables.cell_value(row, col)
    return actual_data


def write_to_excel(file_path, row, col, value):
    work_book = xlrd.open_workbook(file_path, formatting_info=False)
    write_to_work = copy(work_book)
    sheet_data = write_to_work.get_sheet(0)
    sheet_data.write(row, col, str(value))
    write_to_work.save(file_path)


def register_by_phone(link, phone):
    logger("开卡中:链接：{},手机号{}".format(link, phone))
    res = "领取失败"
    link_id = link.split("=")[1]
    base_url = "https://cardapi.dushu.io/WebRedeem/RedeemCard"
    base_data = {
        "id": link_id,
        "name": phone,
        "mobile": phone,
        "positioning": ""
    }
    headers = {
        "user-agent": "Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"}
    try:
        response = requests.post(base_url, data=base_data, headers=headers).json()
        print(response)
        status = str(response['status'])
        print("status", status)
        if status == "0":
            print("message", response['message'])
            if response['message'] == "操作成功":
                res = "开卡成功 \n " \
                      "会员截止日期：{} \n ".format(response['userInfo']['endTimeStr'])
            else:
                res = "开卡失败"
        if status == "7":
            res = "同一类型的读书卡不可重复使用"
        elif status == "2" or status == "6":
            res = "您已经是樊登读书书友"
        elif status == "5":
            res = "该卡仅限首次开通VIP的书友使用"
        elif status == "1":
            res = "该读书卡已被使用"
        elif status == "3":
            res = "无效的读书卡"
        elif status == "4":
            res = "实体卡已过期"
        elif status == "8":
            res = "手机号码格式不正确"
        elif status == "9":
            res = "用户异常，领取失败"

        return res
    except Exception as e:
        print(e)
        return res


def register(phone):
    df = pd.read_excel(link_file_path)
    link_data = []
    for i in df.index.values:  # 获取行号的索引，并对其进行遍历：
        # 根据i来获取每一行指定的数据 并利用to_dict转成字典
        row_data = df.loc[i, ['id', 'link']].to_dict()
        link_data.append(row_data)
    link_data_tem = deepcopy(link_data)
    writer = pd.ExcelWriter(link_file_path, cell_overwrite_ok=True)
    dataframe = DataFrame()

    for index, data in enumerate(link_data):
        link = data['link']
        res = register_by_phone(link, phone)
        if res.startswith("开卡成功"):
            link_data_tem.pop(0)
            res += "请添加客服微信：95499954，另外最新整理的完整书单。"
        else:
            if res == "该读书卡已被使用":
                link_data_tem.pop(0)
                print("该卡已被使用，换卡中")
                continue
            res += "请添加客服微信：95499954"
        if len(link_data_tem) <= 0:
            link_data_tem = [{"id": "", "link": ""}]
        if res == "该读书卡已被使用":
            link_data_tem.pop(0)
        dataframe = dataframe.append(DataFrame(link_data_tem))
        dataframe.to_excel(writer, index=0)
        writer.save()

        return res, len(link_data_tem)

    link_data_tem = [{"id": "", "link": ""}]
    dataframe = dataframe.append(DataFrame(link_data_tem))
    dataframe.to_excel(writer, index=0)
    writer.save()

    return "链接数不足，请添加客服微信：95499954", 0


if __name__ == '__main__':
    # 开卡成功的返回结果
    dic = {'userInfo':
               {'EndTime': 1586258246255, 'UserId': 'kxdiid8vw8io9i8f', 'endTimeStr': '2020.04.07', 'newUser': True,
                'StartTime': 1585048647255, 'startTimeStr': '2020.03.24', 'IsNewUser': True},
           'systemTimeSpan': 1585048647891, 'success': True, 'orderCompletePopupType': 0, 'message': '操作成功',
           'redeemCodeType': 1, 'status': 0, 'statusCode': 200, 'timeUnit': 2}

    res, l = register("15735656018")
    print(res, l)

    # test("https://card.dushu.io/generalize/entityCard/card.html?id=e28ef30a1bbbe013108","15735656005")
