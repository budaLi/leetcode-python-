# @Time    : 2019/12/4 18:31
# @Author  : Libuda
# @FileName: check_link.py
# @Software: PyCharm
import time
from selenium import webdriver
import xlrd
from xlutils.copy import copy
from queue import Queue
import threading

wait_time = 0

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
    global count
    driver = webdriver.Chrome(r"C:\Users\lenovo\PycharmProjects\leetcode-python-\微信公众号\chromedriver.exe")
    while not link_queue.empty():
        index, link = link_queue.get()
        driver.get(link)
        try:
            time.sleep(wait_time)
            text = driver.find_element_by_xpath("/html/body/div[1]/div[1]/p[1]")
            if text.text == "开卡失败":
                write_to_excel(link_file_path, index + 1, link_write_col, "已使用")
                print("该卡已经被使用..{}".format(link))
        except Exception as e:
            count += 1
            res.append(link)
            print("该卡可以使用:{}".format(link))
            # print("当前可使用链接个数为：{}".format(count))



if __name__ == '__main__':
    import time

    start_time = time.time()
    link_queue = Queue()
    print("正在初始化链接队列。。。")
    for i in range(1, link_tables.nrows - 1):
        link_queue.put([i, get_keywords_data(link_tables, i, link_get_col)])
    print("初始化完成")
    res = []
    count = 0

    threads_lis = []
    for i in range(5):
        thread = threading.Thread(target=get_links)
        threads_lis.append(thread)

    for one in threads_lis:
        one.start()

    for one in threads_lis:
        one.join()

    print("当前可用链接数：{}".format(count))
    end_time = time.time()
    print("用时：{}".format(end_time - start_time))
