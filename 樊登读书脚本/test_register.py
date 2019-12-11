# @Time    : 2019/12/11 10:09
# @Author  : Libuda
# @FileName: test_register.py
# @Software: PyCharm
from 樊登读书脚本.all import register

user_agent = "mozilla/5.0 (linux; u; android 4.1.2; zh-cn; mi-one plus build/jzo54k) applewebkit/534.30 (khtml, like gecko) version/4.0 mobile safari/534.30 micromessenger/5.0.1.352"
phone_data = [[phone, 0] for phone in [15099123217, 17621790514]]
y = input("是否设置完毕")
register(phone_data)
