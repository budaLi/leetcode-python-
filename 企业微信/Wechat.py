# @Time    : 2020/3/26 9:32
# @Author  : Libuda
# @FileName: Wechat.py
# @Software: PyCharm

import time
import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder
from 企业微信.config import get_config

config = get_config()


class WeChat:
    def __init__(self):
        """
        参数配置信息可在config.cfg文件中看到
        """
        self.CORPID = config['CORPID']
        self.CORPSECRET = config['CORPSECRET']
        self.AGENTID = config['AGENTID']
        self.TOUSER = config['TOUSER']
        # 发送消息的接口 post请求
        self.send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}'
        # 上传临时素材接口
        self.upload_url = "https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={}&type={}"

    def _get_access_token(self):
        """
        获取access_token
        :return:access_token
        """
        request_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        request_data = {'corpid': self.CORPID,
                        'corpsecret': self.CORPSECRET,
                        }
        response = requests.post(request_url, params=request_data).json()
        if response['errmsg'] == "ok":
            return response["access_token"]
        return response['errmsg']

    def get_access_token(self):
        """
        更新access_token
        先从本地读取
        大于72000s则重新获取
        :return:
        """
        try:
            with open('access_token.conf', 'r') as f:
                t, access_token = f.read().split(" ")
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

    def upload_media(self, file_path, file_type):
        """
        上传临时素材  multipart/form-data 上传
        参考：https://blog.csdn.net/Magician_vv/article/details/90478019?depth_1-utm_source=distribute.pc_relevant.none-task&utm_source=distribute.pc_relevant.none-task
        :param file_path: 文件路径
        :param file_type: 文件类型
        :return:图片media_id
        """
        request_url = self.upload_url.format(self.get_access_token(), file_type)
        headers = {}
        multipart_encoder = MultipartEncoder(
            fields={
                # 这里根据服务器需要的参数格式进行修改
                'file': (file_path, open(file_path, 'rb'), file_type),
            },
        )
        headers['Content-Type'] = multipart_encoder.content_type
        response = requests.post(request_url, data=multipart_encoder, headers=headers).json()
        if response['errmsg'] == "ok":
            return response['media_id']
        return response['errmsg']


    def send_data(self, message):
        send_url = self.send_url.format(self.get_access_token())
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

    def send_media_data(self, media_id, msgtype, touser):
        """
        发送图片.音频，视频文件
        分别有图片（image）、语音（voice）、视频（video），普通文件（file）
        :param media_id: 图片media_id  可通过upload_image()获取
        :return:
        """
        send_url = self.send_url.format(self.get_access_token())
        send_values = {
            "touser": touser,
            "msgtype": msgtype,
            "agentid": self.AGENTID,
            msgtype: {
                "media_id": media_id
            },
        }
        send_msges = json.dumps(send_values)
        response = requests.post(send_url, send_msges).json()

        if response['errmsg'] == "ok":
            return response
        return response['errmsg']

    def get_user_id_by_phone(self, phone):
        """
        通过手机号获取其所对应的userid
        权限说明：
            应用须拥有指定成员的查看权限。
        :return:userid
        """
        request_url = "https://qyapi.weixin.qq.com/cgi-bin/user/getuserid?access_token={}".format(
            self.get_access_token())
        request_data = {
            "mobile": phone
        }
        response = requests.post(request_url, data=json.dumps(request_data)).json()
        if response['errmsg'] == "ok":
            return response['userid']
        return response['errmsg']

    def create_menu(self):
        """
        创建菜单
        :return:
        """
        request_url = "https://qyapi.weixin.qq.com/cgi-bin/menu/create?access_token={}&agentid={}".format(
            self.get_access_token(), self.AGENTID)
        request_data1 = {
            "button": [
                {
                    "name": "扫码",
                    "sub_button": [
                        {
                            "type": "scancode_waitmsg",
                            "name": "扫码带提示",
                            "key": "rselfmenu_0_0",
                            "sub_button": []
                        },
                        {
                            "type": "scancode_push",
                            "name": "扫码推事件",
                            "key": "rselfmenu_0_1",
                            "sub_button": []
                        },
                    ]
                },
                {
                    "name": "发图",
                    "sub_button": [
                        {
                            "type": "pic_sysphoto",
                            "name": "系统拍照发图",
                            "key": "rselfmenu_1_0",
                            "sub_button": []
                        },
                        {
                            "type": "pic_photo_or_album",
                            "name": "拍照或者相册发图",
                            "key": "rselfmenu_1_1",
                            "sub_button": []
                        },
                        {
                            "type": "pic_weixin",
                            "name": "微信相册发图",
                            "key": "rselfmenu_1_2",
                            "sub_button": []
                        }
                    ]
                },
                {
                    "name": "发送位置",
                    "type": "location_select",
                    "key": "rselfmenu_2_0"
                }
            ]
        }
        request_data2 = {
            "button": [
                {
                    "type": "click",
                    "name": "今日歌曲",
                    "key": "V1001_TODAY_MUSIC"
                },
                {
                    "name": "菜单",
                    "sub_button": [
                        {
                            "type": "view",
                            "name": "搜索",
                            "url": "http://www.soso.com/"
                        },
                        {
                            "type": "click",
                            "name": "赞一下我们",
                            "key": "V1001_GOOD"
                        }
                    ]
                }
            ]
        }
        # 传入的data需要是json格式
        response = requests.post(request_url, data=json.dumps(request_data2)).json()
        if response['errmsg'] == "ok":
            return response
        return response['errmsg']


if __name__ == '__main__':
    wx = WeChat()
    # res = wx.create_menu()
    userid = wx.get_user_id_by_phone("15735656005")
    print(userid)
    #
    media = wx.upload_media("3.mp4", 'video')
    print(media)

    res2 = wx.send_media_data(media, "video", userid)
    print(res2)
