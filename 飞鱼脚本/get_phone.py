import requests
import time
import xlrd
from xlutils.copy import copy

start_date = time.mktime(time.strptime("2019-11-1 18:00:00", "%Y-%m-%d %H:%M:%S"))  # 结束时间
end_date = time.mktime(time.strptime("2019-12-12 18:00:00", "%Y-%m-%d %H:%M:%S"))  # 结束时间
phone_file_path = r"C:\Users\qi\Desktop\adb微信加好友\phone_number.xls"
wait_time = 10  #时间间隔

phone_excel = xlrd.open_workbook(phone_file_path)
phoe_tables = phone_excel.sheet_by_index(0)
phone_write_col = 1
phone_can_use_index = phoe_tables.nrows
totle_break_set=set()


def write_to_excel(file_path, row, col, value):
    work_book = xlrd.open_workbook(file_path, formatting_info=False)
    write_to_work = copy(work_book)
    sheet_data = write_to_work.get_sheet(0)
    sheet_data.write(row, col, str(value))
    write_to_work.save(file_path)


def get_new_phone(start, end):
    global phone_can_use_index
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
                if one['telphone'] not in totle_break_set:
                    timeStamp = int(one['create_time'])
                    timeArray = time.localtime(timeStamp)
                    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                    write_to_excel(phone_file_path,phone_can_use_index,phone_write_col-1,otherStyleTime)
                    write_to_excel(phone_file_path,phone_can_use_index,phone_write_col,one['telphone'])
                    res.append([one['telphone'], otherStyleTime])
                    totle_break_set.add(one['telphone'])
                    phone_can_use_index+=1
        else:
            break
    print("新爬取手机号{}个".format(len(res)))
    print("手机号:{}".format(res))
    return res


if __name__ == '__main__':
    crawl_count = 1
    while 1:
        if crawl_count == 1:
            print("第1次爬取")
            # 测试
            get_new_phone(start_date, end_date)
            crawl_count += 1
        else:
            print("第{}次爬取".format(crawl_count))
            times = int(time.time())
            get_new_phone(end_date, times)
            crawl_count += 1

        time.sleep(wait_time)

