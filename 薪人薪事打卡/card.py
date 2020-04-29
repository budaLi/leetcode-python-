# @Time    : 2020/4/29 14:38
# @Author  : Libuda
# @FileName: card.py
# @Software: PyCharm
import requests
import time


def get_code(mobile):
    url = "https://e.xinrenxinshi.com/site/ajax-send-sms-code/login"
    mobile = "+86-" + str(mobile)
    data = {
        "mobile": mobile
    }
    response = requests.post(url=url, data=data).json()
    print(response)
    coid_id = response['data']['code_id']
    return mobile, coid_id


def login(mobile, coid_id, code):
    url = "https://e.xinrenxinshi.com/site/ajax-login"
    data = {
        "mobile": mobile,
        "verify_code": code,
        "verify_code_id": coid_id,
        "verifyLanguageCodeId": "",
        "type": "1"

    }
    response = requests.post(url=url, data=data)
    print(response.text)


def get_x_y():
    url = "https://api.map.baidu.com/location/ip?qt=loc&coor=bd09ll&ak=Er8iGG4UMfSd3Ckuc6w8C56peI4ge1Ih&timeout=10000&callback=_cbk54880"
    response = requests.get(url).text

    response = eval(response[23:-1])
    print(response)
    x, y = response['content']["point"]['x'], response['content']["point"]['y']

    return x, y


def get_csrf_token():
    url = "https://e.xinrenxinshi.com/env/ajax-common?timestamp=1588144329000&app_key=employee&sign_method=md5&version=1.0.0&sign=93740301c08661e7503dab361d7cd8f8"
    headers = {
        "cookie": "QJYDSID=0b32ba0a549e41d7b6f1e57c9a851ab1_247cf3ae48d4464597a0dd764b60c755"
    }
    response = requests.get(url, headers=headers).json()
    print(response)
    csrf = response['data']['csrf']

    return csrf


def card(x, y):
    url = "https://e.xinrenxinshi.com/attendance/ajax-sign"
    timestamp = str(int(time.time() * 100))
    data = {
        "accuracy": "150",
        "latitude": x,
        "longitude": y,
        "macAddr": "",
        "signature": "YGWFEU67HCDKeFa+fnOLoAjvCDE=",
        "timestamp": timestamp
    }
    response = requests.post(url=url, data=data)
    print(response.text)


if __name__ == '__main__':
    mobile = 15735656005
    # x,y =get_x_y()
    x, y = 40.0647820300, 116.1822295900
    print(x, y)
    s = get_csrf_token()
    print(s)
    # res = card(x,y)
    # print(res)
    # mobile,code_id = get_code(mobile)
    # code = input("请输入验证码")
    # response = login(mobile,code_id,code)
    # print(response)
# mobile:
#
#
#
#
#
# // cesf token
# https://e.xinrenxinshi.com/env/ajax-common
# Cookie:QJYDSID=009c6397c5cb464284639ff0e8209918
# Referer:https://e.xinrenxinshi.com/index
#
#
# //经纬度查询
# https://api.map.baidu.com/location/ip?qt=loc&coor=bd09ll&ak=Er8iGG4UMfSd3Ckuc6w8C56peI4ge1Ih&timeout=10000&callback=_cbk54880
#
#
# //签到
# https://e.xinrenxinshi.com/attendance/ajax-sign
# longitude:116.39125750387659
# latitude:39.90714260173349
