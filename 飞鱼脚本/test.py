# @Time    : 2019/12/6 13:36
# @Author  : Libuda
# @FileName: mytest.py
# @Software: PyCharm
import datetime

a = "2019 / 12 / 05 22:24:35"
s = datetime.datetime.strptime(a, "%Y / %m / %d %H:%M:%S")
print(s)
