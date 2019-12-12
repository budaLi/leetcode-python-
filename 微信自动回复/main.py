# @Time    : 2019/12/12 15:54
# @Author  : Libuda
# @FileName: main.py
# @Software: PyCharm
import itchat


@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    return msg.text


itchat.auto_login()
itchat.run()
