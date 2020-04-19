# @Time    : 2020/4/14 15:42
# @Author  : Libuda
# @FileName: main.py
# @Software: PyCharm

import requests
import json


class SendSms:
    def __init__(self, api_key):
        self.api_key = api_key
        self.sing_send_url = 'https://sms.yunpian.com/v2/sms/single_send.json'

    def send(self, code, mobile):
        params = {
            'apikey': self.api_key,
            'mobile': mobile,
            'text': '【李晋军test】您的验证码是{}。如非本人操作，请忽略本短信'.format(code)
        }
        response = requests.post(self.sing_send_url, data=params)
        resurt = json.loads(response.text)
        return resurt


if __name__ == '__main__':
    sendsms = SendSms('65e7be01db4174b372508587a2e2c933')
    res = sendsms.send('1234', '15735656005')
    print(res)
