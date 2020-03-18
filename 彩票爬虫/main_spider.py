# @Time    : 2020/3/18 13:00
# @Author  : Libuda
# @FileName: main_spider.py
# @Software: PyCharm
import requests
import datetime
import csv
import json
import xlrd
from xlutils.copy import copy

base_url = "https://pk10tv.com/pks/getPksHistoryList.do?date={}&lotCode=xyft"
start_date = datetime.datetime(2020, 2, 18)  # 起始时间
end_date = datetime.datetime(2020, 3, 18)  # 结束时间
txt_name = "res.csv"  # 保存csv的路径
# 时间间隔 每隔一天爬一次就可以
delta_date = datetime.timedelta(hours=24)


# start_stamp = start_date
# end_stamp = start_date
def get_keywords_data(tables, row, col):
    actual_data = tables.cell_value(row, col)
    return actual_data


def write_to_excel(file_path, row, col, value):
    work_book = xlrd.open_workbook(file_path, formatting_info=False)
    write_to_work = copy(work_book)
    sheet_data = write_to_work.get_sheet(0)
    sheet_data.write(row, col, str(value))
    write_to_work.save(file_path)



with open(txt_name, 'a+', newline='') as f:
    writer = csv.writer(f)
    row_item = ["" for _ in range(3)]
    row_item[0] = "时间"
    row_item[1] = "期数"
    row_item[2] = "开奖结果"
    writer.writerow(row_item)

while start_date <= end_date:
    print("start:{}".format(start_date))
    url = base_url.format(start_date.strftime("%Y-%m-%d"))
    response = requests.get(url).text
    response = json.loads(response)
    datas = response['result']['data'][::-1]

    for one in datas:
        filter_time = map(int, one['preDrawTime'].split(" ")[0].split("-"))
        if datetime.datetime(*filter_time) > end_date:
            continue
        with open(txt_name, 'a', newline='') as f:
            writer = csv.writer(f)
            row_item = ["" for _ in range(3)]
            row_item[0] = one['preDrawTime']
            row_item[1] = one['preDrawIssue']
            row_item[2] = one['preDrawCode']
            # print(row_item)
            writer.writerow(row_item)
    start_date += delta_date

print("ok")
