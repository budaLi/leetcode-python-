# @Time    : 2019/12/10 18:35
# @Author  : Libuda
# @FileName: new_check_link.py
# @Software: PyCharm

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
    link_data = [get_keywords_data(link_tables, i, link_get_col) for i in range(1, link_tables.nrows)]
    for index, link in enumerate(link_data):

        try:
            print(link)
            response = requests.get(link).content
            soup = BeautifulSoup(response.decode('utf-8'), "html.parser")
            print(soup.find(class_='mobile').get_text())

        except Exception as e:
            print(e)
            count += 1
            res.append(link)
            print("该卡可以使用:{}".format(link))
    print("当前可使用链接个数为：{}".format(count))
    return res


if __name__ == '__main__':
    get_links()
