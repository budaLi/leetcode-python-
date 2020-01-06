# @Time    : 2020/1/6 16:54
# @Author  : Libuda
# @FileName: 快手刷红星.py
# @Software: PyCharm
import time
from adb微信加好友.main import Adb

adb = Adb()

try:
    while 1:
        adb.click_by_text_after_refresh("去浏览")
        time.sleep(3)
        adb.swipe()
        time.sleep(3)
        adb.swipe()
        time.sleep(3)
        adb.swipe()
        time.sleep(3)
        adb.swipe()
except Exception:
    pass


def 去浏览():
    print(123)
