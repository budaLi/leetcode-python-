# @Time    : 2019/12/4 18:31
# @Author  : Libuda
# @FileName: check_link.py
# @Software: PyCharm
import time
from selenium import webdriver
import xlrd
from xlutils.copy import copy

wait_time = 3
driver = webdriver.Chrome(r"C:\Users\lenovo\PycharmProjects\Spider\chromedriver.exe")
link_file_path = r"C:\Users\lenovo\PycharmProjects\leetcode-python-\樊登读书脚本\link.xls"
phone_file_path = r"C:\Users\lenovo\PycharmProjects\leetcode-python-\樊登读书脚本\phone_number.xls"
link_ecel = xlrd.open_workbook(link_file_path)
link_tables = link_ecel.sheet_by_index(0)
link_get_col = 2
link_write_col = 3

phone_excel = xlrd.open_workbook(phone_file_path)
phoe_tables = phone_excel.sheet_by_index(0)
phone_get_col = 1
phone_write_col = 2

phone_can_use_index = 0
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
    count = 0
    link_data = [get_keywords_data(link_tables, i, link_get_col) for i in range(1, link_tables.nrows)]
    for index, link in enumerate(link_data):
        driver.get(link)
        time.sleep(wait_time)
        try:
            text = driver.find_element_by_xpath("/html/body/div[1]/div[1]/p[1]")
            if text.text == "开卡失败":
                write_to_excel(link_file_path, index + 1, link_write_col, "已使用")
                print("该卡已经被使用..{}".format(link))
        except Exception as e:
            count += 1
            print("该卡可以使用:{}".format(link))
    print("当前可使用链接个数为：{}".format(count))
    return count


if __name__ == '__main__':
    get_links()
