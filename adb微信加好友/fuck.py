# @Time    : 2019/12/20 14:49
# @Author  : Libuda
# @FileName: fuck.py
# @Software: PyCharm
from adb微信加好友.main import Adb

adb = Adb()
res = []

bounds = adb.find_node_by_text("发送")
i = 1
while 1:
    for i in range(1, 9):
        for j in range(1, i):
            tem = str(i) + "*" + str(j) + "=" + str(i * j)
            print(tem)
            adb.adb_input(tem)
            adb.click_use_bounds(bounds)
            # bounds = adb.find_node_by_text("发送")
            # while 1:
            #     adb.adb_input("dudu  i am sorry ")
            #     adb.click_use_bounds(bounds)
