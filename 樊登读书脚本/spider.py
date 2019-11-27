# @Time    : 2019/11/26 20:39
# @Author  : Libuda
# @FileName: spider.py
# @Software: PyCharm
import xlrd
from xlutils.copy import copy
from selenium import webdriver
import time
driver = webdriver.Chrome(r'C:\Users\lenovo\PycharmProjects\Spider\chromedriver.exe')

link_file_path = r"C:\Users\lenovo\PycharmProjects\leetcode-python-\樊登读书脚本\link.xls"
phone_file_path = r'C:\Users\lenovo\PycharmProjects\leetcode-python-\樊登读书脚本\phone_number.xls'

link_ecel = xlrd.open_workbook(link_file_path)
link_tables = link_ecel.sheet_by_index(0)
link_get_col = 2
link_write_col = 3

phone_excel = xlrd.open_workbook(phone_file_path)
phoe_tables = phone_excel.sheet_by_index(0)
phone_get_col = 1
phone_write_col = 2
wait_time = 2

phone_can_use_index = 0


def get_keywords_data(tables, row, col):
    actual_data = tables.cell_value(row, col)
    return actual_data


def write_to_excel(file_path, row, col, value):
    work_book = xlrd.open_workbook(file_path, formatting_info=False)
    write_to_work = copy(work_book)
    sheet_data = write_to_work.get_sheet(0)
    sheet_data.write(row, col, str(value))
    write_to_work.save(file_path)


link_data = [get_keywords_data(link_tables, i, link_get_col) for i in range(1, link_tables.nrows)]
phone_data = [str(int(get_keywords_data(phoe_tables, i, phone_get_col))) for i in range(1, phoe_tables.nrows)]

has_phone = True
for index, link in enumerate(link_data):

    if has_phone:
        driver.get(link)
        try:
            text = driver.find_element_by_xpath("/html/body/div[1]/div[1]/p[1]")
            if text.text == "开卡失败":
                write_to_excel(link_file_path, index + 1, link_write_col, "已使用")
                print("该卡已经被使用")
                continue
            else:
                # print(text.text)
                continue
        except Exception as e:
            pass
            # print(e)
        try:
            print("该卡可以使用，正在查询可用手机号。。")
            text = driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/p')
            if text.text == "欢迎加入樊登读书，即刻获得":
                flag = True
                while flag:
                    for ph_number_index in range(phone_can_use_index, len(phone_data)):
                        driver.get(link)
                        print("当前查询手机号为{}".format(phone_data[ph_number_index]))
                        driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[1]/input').send_keys(
                            phone_data[ph_number_index])
                        driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[3]/input').send_keys(
                            phone_data[ph_number_index])
                        driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[3]').click()
                        time.sleep(wait_time)
                        # 点击开卡
                        driver.find_element_by_xpath('//*[@id="join-btn"]').click()
                        time.sleep(wait_time)
                        try:
                            tem = driver.find_element_by_xpath('/html/body/div[1]/div[1]/p[1]')
                            if tem.text == "开卡失败":
                                print("开卡失败，您已经是樊登读书好友")
                                write_to_excel(phone_file_path, ph_number_index + 1, phone_write_col, "开卡失败您已经是樊登读书书友")
                        except Exception:
                            try:
                                print("开卡成功")
                                write_to_excel(link_file_path, index + 1, link_write_col, "成功领取")
                                write_to_excel(phone_file_path, phone_can_use_index + 1, phone_write_col, "开卡成功")
                                has_phone = True
                                flag = False
                            except Exception:
                                print("e")
                    print("当前手机号已全被使用")
                    has_phone = False
                    flag = False

            else:
                # print(text.text)
                continue
        except Exception as e:
            pass
            # print(e)
