# @Time    : 2020/3/5 12:30
# @Author  : Libuda
# @FileName: 远程服务器文件监控.py
# @Software: PyCharm
import os
import time
import win32gui
import win32api
import win32con

# 设置appdict
pyexe = "E:\...\python.exe"
appdict = {'qq': '"D:\...\QQScLauncher.exe"',
           'pl/sql': '"E:\...\plsqldev.exe"',
           'idea': '"E:...\idea64.exe"',
           'chrome': '"C:\...\chrome.exe"'}
# qq登录按钮位置，pl/sql取消按钮位置，idea第一个工程的位置
coorddict = {'qq': [960, 665], 'pl/sql': [1060, 620], 'idea': [700, 245]}
namedict = {'qq': 'QQ', 'pl/sql': 'Oracle Logon', 'idea': 'Welcome to IntelliJ IDEA'}


# 打开应用并且鼠标点击按钮（获取按钮的像素坐标很麻烦）
def open_by_grab():
    pyhd = win32gui.FindWindow("TXGuiFoundation ", u'查找')  # 360会拦截pyexe,可以添加信任或者关闭360
    # 设置pyexe窗口属性和位置，太大会挡住一些窗口
    win32gui.SetWindowPos(pyhd, win32con.HWND_TOPMOST, 0, 0, 500, 500, win32con.SWP_SHOWWINDOW)
    print("py exe 句柄: %s ..." % pyhd)
    for key in appdict.keys():
        print("启动 %s ..." % key)
        os.popen(r'%s' % appdict[key])  # os.system会阻塞
        time.sleep(3)
        if key == "chrome":
            pass
        else:
            winhd = win32gui.FindWindow(None, namedict[key])  # 根据窗口名获取句柄
            while winhd == 0:
                print("等待获取%s窗口 ..." % key)
                time.sleep(3)
                winhd = win32gui.FindWindow(None, namedict[key])
            print("获取%s窗口成功,开始登录 ..." % key)
            a, b = coorddict[key]
            mouse_click(a, b)
            time.sleep(3)
    print("完毕 ...")
    time.sleep(1)
    win32gui.SendMessage(pyhd, win32con.WM_CLOSE)


# 模拟鼠标点击
def mouse_click(a, b):
    time.sleep(1)
    win32api.SetCursorPos((a, b))
    time.sleep(1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)  # 360会拦截虚拟按键,可以添加信任或者关闭360
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def test():
    classname = "TXGuiFoundation"
    titlename = "查找"
    # 获取句柄
    hwnd = win32gui.FindWindow(classname, titlename)
    # 获取窗口左上角和右下角坐标
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    print(left, top, right, bottom)

    # win32api.SendMessage(hwnd, win32con.WM_SETTEXT, 0, "ss".encode('gbk'))


if __name__ == '__main__':
    from pywinauto.application import Application

    # Run a target application
    try:
        app = Application().start("D:\Bin\QQScLauncher.exe")
        # Select a menu item
        app.UntitledNotepad.menu_select("帮助(&H)")
        # Click on a button
        app.AboutNotepad.Edit.click()
        # Type a text string
        app.UntitledNotepad.Edit.type_keys("pywinauto Works!", with_spaces=True)
    except Exception as e:
        print(e)
