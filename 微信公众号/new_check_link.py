# @Time    : 2019/12/10 18:35
# @Author  : Libuda
# @FileName: new_check_link.py
# @Software: PyCharm
import time
from bs4 import BeautifulSoup
import requests
import xlrd
from xlutils.copy import copy

link_file_path = r"C:\Users\lenovo\PycharmProjects\leetcode-python-\微信公众号\link.xls"
link_ecel = xlrd.open_workbook(link_file_path)
link_tables = link_ecel.sheet_by_index(0)
link_get_col = 2
link_write_col = 3
link_can_use_index = 1

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

def get_keywords_data(tables, row, col):
    actual_data = tables.cell_value(row, col)
    return actual_data


def write_to_excel(file_path, row, col, value):
    work_book = xlrd.open_workbook(file_path, formatting_info=False)
    write_to_work = copy(work_book)
    sheet_data = write_to_work.get_sheet(0)
    sheet_data.write(row, col, str(value))
    write_to_work.save(file_path)


def get_links():
    res = []
    count = 0
    link_data = [get_keywords_data(link_tables, i, link_get_col) for i in range(1, link_tables.nrows - 1)]
    for index, link in enumerate(link_data):
        response = requests.get(link, headers=headers).content

        # print(response)
        soup = BeautifulSoup(response.decode('utf-8'), "html.parser")

        # time.sleep(1)
        if soup.find("input", class_='mobile'):

            # print(soup.find("input",class_='mobile'))
            count += 1
            res.append(link)
            print("该卡可以使用:{}".format(link))
        else:
            print("该链接已使用".format(link))
            write_to_excel(link_file_path, index, link_write_col, "已使用")
    print("当前可使用链接个数为：{}".format(count))
    return res


if __name__ == '__main__':
    start_time = time.time()
    get_links()
    end_time = time.time()
    print("时间：{}".format(end_time - start_time))
