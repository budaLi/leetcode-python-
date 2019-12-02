import xlrd
from xlutils.copy import copy
from selenium import webdriver
import time
import schedule
import pandas
import datetime

wait_time = 3  # 各个阶段等待时间
time_jiange= 60 #时间间隔
driver = webdriver.Chrome(r"C:\Users\qi\Desktop\all\chromedriver.exe")
link_file_path = r"C:\Users\qi\Desktop\all\link.xls"
phone_file_path = r"C:\Users\qi\Desktop\all\phone_number.xls"

link_ecel = xlrd.open_workbook(link_file_path)
link_tables = link_ecel.sheet_by_index(0)
link_get_col = 2
link_write_col = 3

phone_excel = xlrd.open_workbook(phone_file_path)
phoe_tables = phone_excel.sheet_by_index(0)
phone_get_col = 1
phone_write_col = 2


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

def get_phone_number(end_date):
    phone_num=13628398278
    #driver = webdriver.Chrome(r'E:\【樊登读书】\【python程序】\抖音后台客户电话导出\houtai\chromedriver.exe')
    df = pandas.DataFrame()
    #file_path =r"E:\【樊登读书】\【python程序】\抖音后台客户电话导出\houtai\锦集20191130.xls"
    driver.get("https://e.douyin.com/site/")
    print("请您进行登录及手动进行所有的筛选")
    yes = input("您是否已确认进行爬取")
    if yes=="y":
        all_data_len = driver.find_element_by_xpath('//*[@id="root"]/div[2]/div[1]/div/div/div[3]/div[1]/div[2]/div[3]/div/div/div/div/div/ul/li[1]').text.split("条")[0].split("共")[1]
        print("总共 {} 条数据".format(all_data_len))
        num_tem = '//*[@id="root"]/div[2]/div[1]/div/div/div[3]/div[1]/div[2]/div[3]/div/div/div/div/div/div/div/div[1]/div/table/tbody/tr[{}]/td[4]'
        date_tem = '//*[@id="root"]/div[2]/div[1]/div/div/div[3]/div[1]/div[2]/div[3]/div/div/div/div/div/div/div/div[1]/div/table/tbody/tr[{}]/td[6]'
        flag = True
        
        while flag:
            time.sleep(wait_time)  #时间间隔
            res_data = []
            for i in range(1,11):
                res_dic = {}
                res_dic['phone_number'] = driver.find_element_by_xpath(num_tem.format(i)).text
                res_dic['date'] = datetime.datetime.strptime(driver.find_element_by_xpath(date_tem.format(i)).text,"%Y.%m.%d %H-%M-%S")
                
                if res_dic['date']>end_date:
                    flag= False
                    break
                res_data.append(res_dic)
            df = df.append(res_data)
            df.to_excel(phone_file_path,index=0)
            print("已写入{}数据".format(len(df)))
            #点击下一页
            try:
                driver.find_element_by_css_selector('.ant-pagination-next').click()
            except Exception as e :
                try:
                    driver.find_element_by_xpath('//*[@id="root"]/div[2]/div[1]/div/div/div[3]/div[1]/div[2]/div[3]/div/div/div/div/div/ul/li[12]').click()
                except Exception:
                    driver.find_element_by_xpath('//*[@id="root"]/div[2]/div[1]/div/div/div[3]/div[1]/div[2]/div[3]/div/div/div/div/div/ul/li[10]').click()

def register():
    global  phone_can_use_index
    link_data = [get_keywords_data(link_tables, i, link_get_col) for i in range(1, link_tables.nrows)]
    phone_data = [str(int(get_keywords_data(phoe_tables, i, phone_get_col))) for i in range(1, phoe_tables.nrows)]

    has_phone = True
    for index, link in enumerate(link_data):

        if has_phone:
            driver.get(link)
            time.sleep(wait_time)
            try:
                text = driver.find_element_by_xpath("/html/body/div[1]/div[1]/p[1]")
                if text.text == "开卡失败":
                    write_to_excel(link_file_path, index + 1, link_write_col, "已使用")
                    print("该卡已经被使用..{}".format(link))
                    continue
                else:
                    # print(text.text)
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
                        q = phone_can_use_index
                        for ph_number_index in range(q, len(phone_data)):
                            driver.get(link)
                            print("当前查询手机号为{}".format(phone_data[ph_number_index]))
                            time.sleep(wait_time)
                            driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[1]/input').send_keys(
                                phone_data[ph_number_index])
                            driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[3]/input').send_keys(
                                phone_data[ph_number_index])
                            driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[3]').click()
                            time.sleep(wait_time)
                            # 点击开卡
                            driver.find_element_by_xpath('//*[@id="join-btn"]').click()
                            # 点击开卡后页面延迟较为严重
                            time.sleep(wait_time)
                            try:
                                tem = driver.find_element_by_xpath('/html/body/div[1]/div[1]/p[1]')
                                if tem.text == "开卡失败":
                                    phone_can_use_index +=1
                                    print("开卡失败，您已经是樊登读书好友")
                                    write_to_excel(phone_file_path, ph_number_index + 1, phone_write_col, "开卡失败您已经是樊登读书书友")
                            except Exception as e:
                                # print(e)
                                time.sleep(wait_time)
                                try:
                                    if driver.find_element_by_xpath('/html/body/div[1]/div/h1').text == "领取成功！":
                                        print("开卡成功")
                                        write_to_excel(link_file_path, index + 1, link_write_col, "领取成功")
                                        write_to_excel(phone_file_path, phone_can_use_index + 1, phone_write_col, "领取成功")
                                        phone_can_use_index += 1
                                        has_phone = True
                                        flag = False
                                        continue
                                except Exception as e:
                                    print("此电话号码有问题")
                                    # write_to_excel(link_file_path, index + 1, link_write_col, "此电话号码有问题")
                                    write_to_excel(phone_file_path, phone_can_use_index + 1, phone_write_col, "此电话号码有问题")
                                    phone_can_use_index += 1
                                    has_phone = True
                                    flag = False
                                    continue
                                    # print(e)
                        print("当前手机号已全被使用")
                        if phone_can_use_index == len(phone_data):
                            has_phone = False
                        flag = False

                else:
                    # print(text.text)
                    continue
            except Exception as e:
                pass
                # print(e)
                
                
if __name__ == '__main__':
    while 1:
        crawl_count = 0
        now_time = time.time()
        # end_date = now_time- time_jiange
        times = datetime.datetime.fromtimestamp(now_time)
        print(times)
        time_str = "{}-{}-{} {}:{}:{}".format(times.year,times.month,times.day-1,0,0,0)
        time_str= datetime.datetime.strptime(time_str,"%Y-%m-%d %h:%M:%S")
        print(time_str)
        if crawl_count==0:
            "第一次爬取"
            get_phone_number(time_str)
            register()
            crawl_count+=1
        else:
            now_time = time.time()-time_jiange
            times = datetime.datetime.fromtimestamp(now_time)
            get_phone_number(times)
            register()
    #schedule.every().day.at('17:49').do(job4)
    #schedule.every(180).seconds.do(get_phone_number)
    #while True:
     #   schedule.run_pending()
    