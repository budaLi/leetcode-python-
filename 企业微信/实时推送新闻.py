#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import requests
import json
from datetime import datetime
from 企业微信.邮件接收程序 import logger
from 企业微信.config import get_config
from 企业微信.spider import spider

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

    # 接收内容
    l, res = spider()
    # while 1:
    #     new_l, new_res = spider()
    #     if res!=new_res:
    #         print("{}:{}".format(time.ctime(), new_res))
    #         res = new_res
    #     else:
    #         print("{},新闻：{}".format(time.ctime(),l))
    #     time.sleep(300)

    while 1:
        current_time = datetime.now().time()

        # logger("检测新闻中")
        try:
            new_l, new_res = spider()
            if new_res and res != new_res:
                logger("{}".format(new_res))
                res = new_res
                wx.send_data(new_res)
            else:
                logger("{},新闻：{}".format(time.ctime(), l))
            time.sleep(int(config['sleep']))
        except Exception as e:
            print("运行错误", e)
