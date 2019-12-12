# @Time    : 2019/12/2 11:17
# @Author  : Libuda
# @FileName: spider.py
# @Software: PyCharm
import xlrd
from xlutils.copy import copy
from selenium import webdriver
import time
from 飞鱼脚本.sendEmail import SendEmail
from copy import deepcopy
import requests

user_agent = "mozilla/5.0 (linux; u; android 4.1.2; zh-cn; mi-one plus build/jzo54k) applewebkit/534.30 (khtml, like gecko) version/4.0 mobile safari/534.30 micromessenger/5.0.1.352"
url = "https://feiyu.oceanengine.com/feiyu/login"
send = SendEmail()
user_list = ['1364826576@qq.com']

phone_num = 13281890000
wait_time = 3  # 各个阶段等待时间
time_jiange = 30  # 时间间隔 隔多长时间执行脚本一次
start_date = time.mktime(time.strptime("2019-11-1 18:00:00", "%Y-%m-%d %H:%M:%S"))  # 结束时间
end_date = time.mktime(time.strptime("2019-12-12 18:00:00", "%Y-%m-%d %H:%M:%S"))  # 结束时间
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


def get_new_phone(start, end):
    res = []
    headers = {
        "cookie": "ccid=ac428488c168899d07df951f7354ba55; msh=GqsdyEcveB1HjZLIZKT5ALDFoAE; sso_auth_status=26a7e62720484fd24d45830a4b543edb; sso_uid_tt=89b572982452ca2533fc5c49e4a3540e; toutiao_sso_user=4cd8bb9233af1784dbf3f269d15233d8; passport_auth_status=9f2216029d9ce53808046ea02135feff%2C7f9ddb5f3555a4e4db4cae3b62ed1213; sid_guard=3c3144f57c28219795bc821cf887fc79%7C1576146759%7C5184000%7CMon%2C+10-Feb-2020+10%3A32%3A39+GMT; uid_tt=e239ea11351745eb4404675817d217c5; sid_tt=3c3144f57c28219795bc821cf887fc79; sessionid=3c3144f57c28219795bc821cf887fc79; toutiao-crm-session=s%3Ab88ca4f2-1cca-11ea-adad-ac1f6b0ad100b88ca4f2-1cca-11ea-adad-ac1f6b0ad100sD3tpStsTyYsYE2aa56BtD22.jjnP%2F%2FLSX4oqXo%2FC15QML%2FFEvTN9OYGUoBHcVGkmgz0; gr_user_id=6892c2d6-d651-4a12-adc2-6c3b37e7c414; gr_session_id_9952092a9d995794=05a5816c-4d44-4447-8e5d-a813f5bd7f61; gr_cs1_05a5816c-4d44-4447-8e5d-a813f5bd7f61=advertiser_id%3A1645790969889795; gr_session_id_9952092a9d995794_05a5816c-4d44-4447-8e5d-a813f5bd7f61=true"}
    base_url = "https://feiyu.oceanengine.com/crm/v2/api/clue/public/?_t=1576147755&page={}&page_size=20&clue_public_status=0&start_time={}&end_time={}"
    i = 1
    while True:
        response = requests.get(base_url.format(i, start, end), headers=headers).json()
        if response['data']:
            i += 1
            for one in response['data']:
                # print(one['telphone'])
                if one['telphone'] not in totle_break_set:
                    timeStamp = int(one['create_time'])
                    timeArray = time.localtime(timeStamp)
                    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                    res.append([one['telphone'], otherStyleTime])
        else:
            break
    print("新爬取手机号{}个".format(len(res)))
    print("手机号:{}".format(res))
    return res



def get_phone_number(star_date, end_date):
    print("当前已使用手机号：{}，使用数量：{}".format(totle_break_set, len(totle_break_set)))
    result = []
    # 搜索按钮
    try:
        driver.find_element_by_xpath(
            '//*[@id="app"]/div/div[2]/div[2]/div[3]/div[1]/div/div[2]/div[2]/div[3]').click()
    except Exception as e:
        print(e)
        pass

    # num_tem = '//*[@id="app"]/div/div[2]/div[2]/div[3]/div[3]/div[2]/div[1]/div/div[2]/table[2]/tr[{}]/td[4]/div/div/div/div/div/span[1]'
    # date_tem = '//*[@id="app"]/div/div[2]/div[2]/div[3]/div[3]/div[2]/div[1]/div/div[1]/table[2]/tr[{}]/td[7]/div/div/div/div'
    #
    # try:
    #     for i in range(10):
    #         time.sleep(2)
    #         phone = driver.find_element_by_xpath(num_tem.format(i))
    #         date = driver.find_element_by_xpath(date_tem.format(i))
    #         print(phone,date)
    # except Exception as e :
    #     print(e,'第一次获取数据异常')

    flag = True
    phone_lis = []
    data_lis = []
    while flag:
        try:
            time.sleep(5)
            phones = driver.find_elements_by_css_selector("span.phone")
            print("len", len(phones))
            for one in phones:
                print("text", one.text)
                if one.text != "":
                    if one.text not in totle_break_set:
                        phone_lis.append(one.text)
                        totle_break_set.add(one.text)
                        data_lis.append("time")
                    else:
                        flag = False
        except Exception as e:
            print("phone", e)
        # try:
        #     dates = driver.find_elements_by_css_selector(".createTime")
        #     for one in dates:
        #         if one.text!="":
        #             # print("time",one.text)
        #             data_lis.append(one.text)
        # except Exception as e:
        #     print("date",e)

        if len(data_lis) < len(phone_lis):
            for i in range(len(phone_lis) - len(data_lis)):
                data_lis.append(time.time())
        print(phone_lis)
        print(data_lis)

        for i in range(len(phone_lis)):
            result.append([data_lis[i], phone_lis[i]])
        try:
            # 这儿要处理
            driver.find_element_by_css_selector('.m-item.previous.next').click()
        except Exception as e:
            flag = False
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

                # # 发邮件
                # send.send_test(user_list, 0)
                # print("链接已经全部用完 请及时补充！")
                # # print(e)


def main():
    crawl_count = 1
    while 1:
        if crawl_count == 1:
            print("第1次爬取")
            # 测试
            phone_data = get_new_phone(start_date, end_date)
            y = input("是否设置完毕")
            register(phone_data)
            crawl_count += 1
        else:
            print("第{}次爬取".format(crawl_count))
            times = int(time.time())
            phone_data = get_new_phone(end_date, times)
            register(phone_data)
            crawl_count += 1

        time.sleep(time_jiange)


if __name__ == '__main__':
    # 主函数
    main()
    # get_new_phone_number(1,1)
