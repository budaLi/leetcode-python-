# @Time    : 2019/12/20 12:25
# @Author  : Libuda
# @FileName: playgame.py
# @Software: PyCharm
from pynput.keyboard import Listener

keys = ""


def press(key):
    global keys
    keys += str(key.char)
    if len(keys) > 10:
        print(keys)


with Listener(on_press=press) as listener:
    listener.join()
