#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import requests
import json
from datetime import datetime, time as dtime
from 企业微信.邮件接收程序 import get_rev, logger
from 企业微信.config import get_config

config = get_config()

class WeChat:
    def __init__(self):
        self.CORPID = config['CORPID']
        self.CORPSECRET = config['CORPSECRET']
        self.AGENTID = config['AGENTID']
        self.TOUSER = config['TOUSER']

    def _get_access_token(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {'corpid': self.CORPID,
                  'corpsecret': self.CORPSECRET,
                  }
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        return data["access_token"]

    def get_access_token(self):
        try:
            with open('access_token.conf', 'r') as f:
                t, access_token = f.read().split()
        except:
            with open('access_token.conf', 'w') as f:
                access_token = self._get_access_token()
                cur_time = time.time()
                f.write('\t'.join([str(cur_time), access_token]))
                return access_token
        else:
            cur_time = time.time()
            if 0 < cur_time - float(t) < 7200:
                return access_token
            else:
                with open('access_token.conf', 'w') as f:
                    access_token = self._get_access_token()
                    f.write('\t'.join([str(cur_time), access_token]))
                    return access_token

    def send_data(self, message):
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token()
        send_values = {
            "touser": self.TOUSER,
            "msgtype": "text",
            "agentid": self.AGENTID,
            "text": {
                "content": message
            },
            "safe": "0"
        }
        send_msges = (bytes(json.dumps(send_values), 'utf-8'))
        respone = requests.post(send_url, send_msges)
        respone = respone.json()  # 当返回的数据是json串的时候直接用.json即可将respone转换成字典
        return respone["errmsg"]

if __name__ == '__main__':
    wx = WeChat()

    # 程序运行时间在白天8:55 到 11:30  下午1:30 到  3:01
    DAY_START = dtime(8, 55)
    DAY_END = dtime(11, 30)

    NIGHT_START = dtime(13, 30)
    NIGHT_END = dtime(23, 59)

    # 接收邮件
    rev = get_rev()

    while 1:
        current_time = datetime.now().time()
        if DAY_START <= current_time <= DAY_END or (NIGHT_START <= current_time <= NIGHT_END):
            # 判断时候在可运行时间内
            logger("等待接收邮件中")
            try:
                content = rev.run_ing()
                if content:
                    print("接收到邮件：{}".format(content))
                    wx.send_data(content)
            except Exception as e:
                print("运行错误", e)
        else:
            time.sleep(2)
            logger("其他时间段  其他任务执行中")
