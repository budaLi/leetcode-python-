# @Time    : 2019/12/2 11:17
# @Author  : Libuda
# @FileName: spider.py
# @Software: PyCharm
import xlrd
from xlutils.copy import copy
from selenium import webdriver
import time
import datetime
from sendEmail import SendEmail
from copy import deepcopy

send = SendEmail()
user_list = ['1364826576@qq.com']

phone_num = 13281890000
wait_time = 3  # 各个阶段等待时间
time_jiange = 30  # 时间间隔 隔多长时间执行脚本一次
start_date = datetime.datetime.strptime("2019-12-1 00:00:00", "%Y-%m-%d %H:%M:%S")  # 起始时间
end_date = datetime.datetime.strptime("2019-12-7 18:00:00", "%Y-%m-%d %H:%M:%S")  # 结束时间
ding_num = 5  # 链接条数报警阈值

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
totle_break_set = set()


def get_keywords_data(tables, row, col):
    actual_data = tables.cell_value(row, col)
    return actual_data


def write_to_excel(file_path, row, col, value):
    work_book = xlrd.open_workbook(file_path, formatting_info=False)
    write_to_work = copy(work_book)
    sheet_data = write_to_work.get_sheet(0)
    sheet_data.write(row, col, str(value))
    write_to_work.save(file_path)


def get_phone_number(star_date, end_date):
    print("当前已使用手机号：{}，使用数量：{}".format(totle_break_set, len(totle_break_set)))
    result = []
    # 搜索按钮
    try:
        driver.find_element_by_xpath(
            '//*[@id="root"]/div[2]/div[1]/div/div/div[3]/div[1]/div[2]/div[2]/div[4]/span[2]/span/span').click()
    except Exception as e:
        print(e)
        pass

    # num_tem = '//*[@id="app"]/div/div[2]/div[2]/div[3]/div[3]/div[2]/div[1]/div/div[2]/table[2]/tr[{}]/td[4]/div/div/div/div'
    # date_tem = '//*[@id="app"]/div/div[2]/div[2]/div[3]/div[3]/div[2]/div[1]/div/div[1]/table[2]/tr[{}]/td[7]'



    flag = True
    phone_lis = []
    data_lis = []
    while flag:
        time.sleep(5)
        try:
            phones = driver.find_elements_by_css_selector(".phone")
            for one in phones:
                phone_lis.append(one.text)
        except Exception as e:
            print(e)
        try:
            dates = driver.find_elements_by_css_selector(".createTime")
            for one in dates:
                data_lis.append(one.text)
        except Exception as e:
            print(e)

        print(phone_lis)
        print(data_lis)

        for i in range(len(phone_lis)):
            result.append([data_lis[i], phone_lis[i]])
        print(result)
        try:
            # 这儿要处理
            driver.find_element_by_css_selector('.m-item.previous.next').click()
        except Exception as e:
            print(e)
            pass

    print("已爬取到新手机号：{}个".format(len(result)))
    print("翻页结束,等待页数回滚中。。。")
    tem_break = deepcopy(totle_break_set)
    pre_flag = True
    while pre_flag:
        try:
            for i in range(20):
                tem_break.pop()
            driver.find_element_by_css_selector('.m-item.previous').click()
            time.sleep(wait_time)
        except Exception as e:
            # print(e)
            pre_flag = False
            print("回滚结束")

    return result


def register(phone_data):
    global phone_can_use_index, link_can_use_index, ding_num
    phone_excel = xlrd.open_workbook(phone_file_path)
    phoe_tables = phone_excel.sheet_by_index(0)
    phone_can_use_index = phoe_tables.nrows
    link_data = [get_keywords_data(link_tables, i, link_get_col) for i in range(link_can_use_index, link_tables.nrows)]
    length = len(phone_data)
    phone_index = 0
    has_phone = True
    for index, link in enumerate(link_data):
        if len(link_data) <= ding_num:
            print("当前链接条数为：{}，当前链接条数不足 请及时补充！".format(len(link_data)))
            send.send_test(user_list, len(link_data))
        if length <= 0:
            print("当前手机号已全被使用")
            break
        ding_num -= 1
        if has_phone:
            driver.get(link)
            time.sleep(wait_time)
            try:
                text = driver.find_element_by_xpath("/html/body/div[1]/div[1]/p[1]")
                if text.text == "开卡失败":
                    write_to_excel(link_file_path, index + 1, link_write_col, "已使用")
                    print("该卡已经被使用..{}".format(link))
                    link_can_use_index += 1
                    continue
                else:
                    write_to_excel(link_file_path, index + 1, link_write_col, "已使用")
                    print("该卡已经被使用..{}".format(link))
                    link_can_use_index += 1
                    continue
            except Exception as e:
                time.sleep(wait_time)
                # print(e)
            try:
                print("该卡可以使用:{}，正在查询可用手机号。。".format(link))
                text = driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/p')
                if text.text == "欢迎加入樊登读书，即刻获得":
                    flag = True
                    while flag:
                        for ph_number_index in range(phone_index, len(phone_data)):
                            driver.get(link)
                            length -= 1
                            phone_index += 1
                            print("当前查询手机号索引为{}，号码为{}".format(ph_number_index, phone_data[ph_number_index][0]))
                            time.sleep(wait_time)
                            driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[1]/input').send_keys(
                                phone_data[ph_number_index][0])
                            driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[3]/input').send_keys(
                                phone_data[ph_number_index][0])
                            driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[3]').click()
                            time.sleep(wait_time)
                            # 点击开卡
                            driver.find_element_by_xpath('//*[@id="join-btn"]').click()
                            # 点击开卡后页面延迟较为严重
                            time.sleep(wait_time)
                            try:
                                tem = driver.find_element_by_xpath('/html/body/div[1]/div[1]/p[1]')
                                if tem.text == "开卡失败":
                                    print("开卡失败，您已经是樊登读书好友")

                                    # 日期
                                    write_to_excel(phone_file_path, phone_can_use_index + 1, phone_write_col - 2,
                                                   phone_data[ph_number_index][1])
                                    # 手机号
                                    write_to_excel(phone_file_path, phone_can_use_index + 1, phone_write_col - 1,
                                                   phone_data[ph_number_index][0])
                                    # 使用状态
                                    write_to_excel(phone_file_path, phone_can_use_index + 1, phone_write_col,
                                                   "开卡失败您已经是樊登读书书友")
                                    phone_can_use_index += 1
                            except Exception as e:
                                # print(e)
                                flag = False
                                time.sleep(wait_time)
                                try:
                                    if driver.find_element_by_xpath('/html/body/div[1]/div/h1').text == "领取成功！":
                                        print("开卡成功")
                                        write_to_excel(link_file_path, index + 1, link_write_col, "领取成功")
                                        # 日期
                                        write_to_excel(phone_file_path, phone_can_use_index + 1, phone_write_col - 2,
                                                       phone_data[ph_number_index][1])
                                        # 手机号
                                        write_to_excel(phone_file_path, phone_can_use_index + 1, phone_write_col - 1,
                                                       phone_data[ph_number_index][0])
                                        # 使用状态
                                        write_to_excel(phone_file_path, phone_can_use_index + 1, phone_write_col,
                                                       "领取成功")
                                        link_can_use_index += 1
                                        phone_can_use_index += 1
                                        has_phone = True
                                        break
                                except Exception as e:
                                    print("此电话号码有问题")
                                    # write_to_excel(link_file_path, index + 1, link_write_col, "此电话号码有问题")
                                    write_to_excel(link_file_path, index + 1, link_write_col, "领取成功")
                                    # 日期
                                    write_to_excel(phone_file_path, phone_can_use_index + 1, phone_write_col - 2,
                                                   phone_data[ph_number_index][1])
                                    # 手机号
                                    write_to_excel(phone_file_path, phone_can_use_index + 1, phone_write_col - 1,
                                                   phone_data[ph_number_index][0])
                                    # 使用状态
                                    write_to_excel(phone_file_path, phone_can_use_index + 1, phone_write_col,
                                                   "此电话号码有问题")
                                    # write_to_excel(phone_file_path, phone_can_use_index + 1, phone_write_col, "此电话号码有问题")
                                    phone_can_use_index += 1
                                    has_phone = True
                                    continue
                                    # print(e)
                        flag = False
                else:
                    # print(text.text)
                    continue
            except Exception as e:
                pass

    # 发邮件
    send.send_test(user_list, 0)
    print("链接已经全部用完 请及时补充！")
    # print(e)


def main():
    crawl_count = 1
    while 1:

        # time_str = datetime.datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        # print(times)
        # # s="2019.12.02 13:56:20"
        # # print(datetime.datetime.strptime(s,"%Y.%m.%d %H:%M:%S")<times)
        if crawl_count == 1:
            now_time = time.time()
            # end_date = now_time- time_jiange
            times = datetime.datetime.fromtimestamp(now_time)
            # time_str = "{}-{}-{} {}:{}:{}".format(times.year, times.month, times.day - 1, 0, 0, 0)
            print("第1次爬取")
            # driver.get("https://e.douyin.com/site/manage-center/user-manage")
            driver.get("https://feiyu.oceanengine.com/feiyu/login")

            print("请您进行登录及手动进行所有的筛选")
            yes = input("您是否已确认进行爬取")
            # cookie= driver.get_cookies()
            # driver.get("https://e.douyin.com/site/manage-center/user-manage")
            phone_data = get_phone_number(start_date, end_date)
            # print([phone for phone in phone_data[0]])
            windows = driver.current_window_handle
            js = 'window.open("https://www.baidu.com");'
            driver.execute_script(js)
            for wins in driver.window_handles:
                if wins != windows:
                    driver.switch_to.window(wins)
            # 测试
            # phone_data = [[phone, 0] for phone in [13945868092, 15169722520]]
            register(phone_data)
            driver.close()
            driver.switch_to.window(windows)

            crawl_count += 1
        else:
            print("第{}次爬取".format(crawl_count))
            now_time = time.time() - time_jiange
            times = datetime.datetime.fromtimestamp(now_time)
            phone_data = get_phone_number(start_date, end_date)
            windows = driver.current_window_handle
            js = 'window.open("https://www.baidu.com");'
            driver.execute_script(js)
            for wins in driver.window_handles:
                if wins != windows:
                    driver.switch_to.window(wins)
            # 测试
            # phone_data = [[phone,0] for phone in [15099123201,17621790591]]
            register(phone_data)
            driver.close()
            driver.switch_to.window(windows)
            crawl_count += 1

        time.sleep(time_jiange)


if __name__ == '__main__':
    # 主函数
    main()
