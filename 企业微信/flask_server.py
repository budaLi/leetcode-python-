# @Time    : 2020/3/5 16:58
# @Author  : Libuda
# @FileName: flask_server.py
# @Software: PyCharm
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# by vellhe 2017/7/9

from flask import Flask, request
from 被动回复 import WXBizMsgCrypt
import xml.etree.cElementTree as ET

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def create_app():
    sToken = "hJqcu3uJ9Tn2gXPmxx2w9kkCkCE2EPYo"
    sEncodingAESKey = "6qkdMrq68nTKduznJYO1A37W2oEgpkMUvkttRToqhUt"
    sCorpID = "wwefe26840c41c9ef8"  # 企业微信的cropid
    wxcpt = WXBizMsgCrypt(sToken, sEncodingAESKey, sCorpID)
    if request.method == 'GET':
        sVerifyMsgSig = request.args.get("msg_signature")
        sVerifyTimeStamp = request.args.get("timestamp")
        sVerifyNonce = request.args.get("nonce")
        sVerifyEchoStr = request.args.get("echostr").replace(" ", "+")
        ret, sEchoStr = wxcpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp, sVerifyNonce, sVerifyEchoStr)

        if ret == 0:
            return sEchoStr
        return "Secho:{}".format(sEchoStr)
    if request.method == "POST":
        sReqMsgSig = request.args.get("msg_signature")
        sReqTimeStamp = request.args.get("timestamp")
        sReqNonce = request.args.get("nonce")
        # sReqData = "<xml><ToUserName><![CDATA[wwefe26840c41c9ef8]]></ToUserName>\n<Encrypt><![CDATA[Kl7kjoSf6DMD1zh7rtrHjFaDapSCkaOnwu3bqLc5tAybhhMl9pFeK8NslNPVdMwmBQTNoW4mY7AIjeLvEl3NyeTkAgGzBhzTtRLNshw2AEew+kkYcD+Fq72Kt00fT0WnN87hGrW8SqGc+NcT3mu87Ha3dz1pSDi6GaUA6A0sqfde0VJPQbZ9U+3JWcoD4Z5jaU0y9GSh010wsHF8KZD24YhmZH4ch4Ka7ilEbjbfvhKkNL65HHL0J6EYJIZUC2pFrdkJ7MhmEbU2qARR4iQHE7wy24qy0cRX3Mfp6iELcDNfSsPGjUQVDGxQDCWjayJOpcwocugux082f49HKYg84EpHSGXAyh+/oxwaWbvL6aSDPOYuPDGOCI8jmnKiypE+]]></Encrypt>\n<AgentID><![CDATA[1000002]]></AgentID>\n</xml>"
        sReqData = request.get_data()
        # print("xml数据",sReqData)
        ret, sMsg = wxcpt.DecryptMsg(sReqData, sReqMsgSig, sReqTimeStamp, sReqNonce)
        # print(sReqMsgSig)
        # print(sReqTimeStamp)
        # print(sReqData)
        # print(ret, sMsg)
        if (ret != 0):
            print("ERR: DecryptMsg ret: " + str(ret))
            return "解析失败"
        xml_tree = ET.fromstring(sMsg)
        print("收到消息:", xml_tree)
        for one in xml_tree:
            print("s", one)
        content = xml_tree.find("Content").text
        fronusername = xml_tree.find("FromUserName").text
        tousername = xml_tree.find("ToUserName").text
        # print("收到消息",content)
        sRespData_tem = "<xml><ToUserName>{}</ToUserName><FromUserName>{}</FromUserName><CreateTime>{}</CreateTime><MsgType>text</MsgType><Content>{}</Content><MsgId>1456453720</MsgId><AgentID>1000002</AgentID></xml>"
        try:
            with open(content) as f:
                content = ",".join(f.readlines())
        except Exception:
            with open("0") as f:
                content = ",".join(f.readlines())
        sRespData = sRespData_tem.format(tousername, fronusername, sReqTimeStamp, content)
        ret, sEncryptMsg = wxcpt.EncryptMsg(sRespData, sReqNonce, sReqTimeStamp)

        if (ret != 0):
            return ("回复错误 " + str(ret))
        return sEncryptMsg


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True
    )
