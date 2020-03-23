# @Time    : 2019/12/12 15:54
# @Author  : Libuda
# @FileName: 远程服务器文件监控.py
# @Software: PyCharm
import itchat


@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    return msg.text


itchat.auto_login()
itchat.run()
