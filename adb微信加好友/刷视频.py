# @Time    : 2019/12/27 15:45
# @Author  : Libuda
# @FileName: 刷视频.py
# @Software: PyCharm
import time
from adb微信加好友.adbtools import Adb

adb = Adb()

while 1:
    adb.swipe()
    adb.click_by_class_name_after_refresh("android.widget.FrameLayout")
    time.sleep(1)
