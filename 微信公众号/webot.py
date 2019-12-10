# @Time    : 2019/12/10 12:00
# @Author  : Libuda
# @FileName: webot.py
# @Software: PyCharm
import requests
from werobot import WeRoBot
import xlrd

from check_link import get_keywords_data

appID = 'wxf74f52d6e57f9e0e'
appsecret = 'c63f351e9a9041d03da9370948de1f16'
token = 'asdfghgfdsaasdfggfdsasdf'
robot = WeRoBot(token=token)

link_file_path = r"C:\Users\lenovo\PycharmProjects\leetcode-python-\微信公众号\link.xls"
link_ecel = xlrd.open_workbook(link_file_path)
link_tables = link_ecel.sheet_by_index(0)
link_get_col = 2
link_write_col = 3
link_data = [get_keywords_data(link_tables, i, link_get_col) for i in range(1, link_tables.nrows)]

openid_file_path = r'C:\Users\lenovo\PycharmProjects\leetcode-python-\微信公众号\openid'


def get_access_token():
    """
    获取accestoken
    :return:
    """
    get_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.format(appID,
                                                                                                               appsecret)
    response = requests.get(get_url).json()
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
    openid_lis = get_user_list()
    if check_user(openid_lis):
        data = link_data.pop()
    else:
        data = '温馨提示：每个用户限领一次14天VIP会员，你已领取。如需帮助，请咨询客服微信：95499954'
    return data


# 其他消息返回
@robot.handler
def hello(message):
    return '(O_o)??'


if __name__ == '__main__':
    robot.config['HOST'] = '0.0.0.0'
    robot.config['PORT'] = 80
    robot.run()
