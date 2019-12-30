# @Time    : 2019/12/30 13:52
# @Author  : Libuda
# @FileName: 刷微信读书时长.py
# @Software: PyCharm
import random
import time
from adb微信加好友.adbtools import Adb

adb = Adb()


# 自动翻页，翻页后休息5-10秒钟
def autoSwipe():
    # 假装看书45-55秒钟(假装是人类在看书。。。)
    read_time = random.randint(5, 10)
    time.sleep(read_time)
    # print("阅读花费：",read_time,"秒")
    adb.swipe([1000, 500], [30, 500])  # 这里需要根据你的模拟器的具体坐标测试


if __name__ == '__main__':
    start_time = time.ctime()
    print("开始时间：{}".format(start_time))
    while 1:
        autoSwipe()
