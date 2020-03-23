# @Time    : 2019/12/10 12:00
# @Author  : Libuda
# @FileName: webot.py
# @Software: PyCharm
import requests
from werobot import WeRoBot
import xlrd
from xlutils.copy import copy
from 微信公众号.check_link import get_keywords_data

appID = 'wxcf14ed85674052e6'
appsecret = '4059313e50fbb08599f4426c23f3b559'
token = 'asdfghgfdsaasdfggfdsasdf'
robot = WeRoBot(token=token)

link_file_path = r"C:\Users\lenovo\PycharmProjects\leetcode-python-\微信公众号\link.xls"
link_ecel = xlrd.open_workbook(link_file_path)
link_tables = link_ecel.sheet_by_index(0)
link_get_col = 2
link_write_col = 3
link_can_write_index = 1
link_data = [get_keywords_data(link_tables, i, link_get_col) for i in range(1, link_tables.nrows)]

openid_file_path = r'C:\Users\lenovo\PycharmProjects\leetcode-python-\微信公众号\openid'


def write_to_excel(file_path, row, col, value):
    work_book = xlrd.open_workbook(file_path, formatting_info=False)
    write_to_work = copy(work_book)
    sheet_data = write_to_work.get_sheet(0)
    sheet_data.write(row, col, str(value))
    write_to_work.save(file_path)

def get_access_token():
    """
    获取accestoken
    :return:
    """
    get_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.format(appID,
                                                                                                               appsecret)
    response = requests.get(get_url).json()
    print(response)
    if 'errcode' in response:
        return False
    elif 'access_token' in response:
        return response['access_token']


def get_user_list():
    """
    获取关注者的openid
    :return:
    """
    openid_lis = []
    acces_token = get_access_token()
    get_url = 'https://api.weixin.qq.com/cgi-bin/user/get?access_token={}&next_openid='.format(acces_token)
    # print(get_url)
    response = requests.get(get_url).json()
    # print(response)
    if 'errcode' in response:
        return openid_lis
    elif 'data' in response:
        openid_lis = response['data']['openid']

    return openid_lis


# 被关注
@robot.subscribe
def subscribe(message):
    data = "回复数字“14”，公众号自动发送一条14天卡链接给客户（每个微信号限领取一个链接)"
    return data


def check_user(openid_lis):
    with open(openid_file_path, 'r') as f:
        data = f.readlines()
    if len(data) == 0:
        for one in openid_lis:
            with open(openid_file_path, 'a') as f:
                f.write(one + "\n")
            return True
    else:
        res = []
        for one in data:
            res.append(one.replace('\n', ''))
        print(res)
        for one in openid_lis:
            if one not in res:
                with open(openid_file_path, 'a') as f:
                    f.write(one + "\n")
                return True
    return False


@robot.filter('14')
def joke():
    global link_can_write_index
    openid_lis = get_user_list()
    if check_user(openid_lis):
        data = link_data.pop()
        write_to_excel(link_file_path, link_can_write_index, link_write_col, data)
        link_can_write_index += 1

    else:
        data = '温馨提示：每个用户限领一次14天VIP会员，你已领取。如需帮助，请咨询客服微信：95499954'
    return data


# 其他消息返回
@robot.handler
def hello(message):
    return '(O_o)??'


if __name__ == '__main__':
    # print(get_access_token())
    robot.config['HOST'] = '127.0.0.1'
    robot.config['PORT'] = 80
    robot.run()
