# @Time    : 2020/4/4 17:13
# @Author  : Libuda
# @FileName: tt.py
# @Software: PyCharm
import win32gui
import win32api
import win32con
import win32clipboard as w
import win32clipboard
import time
import ctypes
import pyautogui

from qq加群.spider import spider

#  安全限制
pyautogui.FAILSAFE = False

# qq_or_wx = "TXGuiFoundation"  qq
# qq_or_wx = "ChatWnd"  #微信
qq_or_wx = "WwStandaloneConversationWnd"  # 企业微信
sleep_time = 60  # 休眠时间
winname = ["阿尔萨斯", "Q", "不搭＊"]  # 需要发送的

add_txt = "\n   ❤ 更多咨询请联系客服微信：876134889"

totol_dic = set()  # 去重


def logger(msg):
    """
    日志信息

    """
    now = time.ctime()
    print("[%s] %s" % (now, msg))


def testss():
    # 获取窗口大小
    hwnd = win32gui.FindWindow(qq_or_wx, winname)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 500, 500, win32con.SWP_SHOWWINDOW)
    win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)

    if win32gui.IsIconic(hwnd):
        logger(">>>窗口已经最小化了")
        win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
        time.sleep(0.1)
        logger(">>>开始虚拟按键操作")

    logger(">>>开始虚拟按键操作")
    win32gui.SetForegroundWindow(hwnd)
    # 设置剪贴板
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, "123")
    win32clipboard.CloseClipboard()
    time.sleep(0.1)
    # 填充消息
    win32gui.PostMessage(hwnd, win32con.WM_CHAR, 22, 2080193)
    win32gui.PostMessage(hwnd, win32con.WM_PASTE, 0, 0)
    time.sleep(0.1)
    # 回车发送消息
    win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    win32gui.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
    time.sleep(0.1)
    # 清空剪贴板
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.CloseClipboard()
    time.sleep(0.5)


def get_window_rect(hwnd):
    try:
        f = ctypes.windll.dwmapi.DwmGetWindowAttribute
    except WindowsError:
        f = None
    if f:
        rect = ctypes.wintypes.RECT()
        DWMWA_EXTENDED_FRAME_BOUNDS = 9
        f(ctypes.wintypes.HWND(hwnd),
          ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
          ctypes.byref(rect),
          ctypes.sizeof(rect)
          )
        return rect.left, rect.top, rect.right, rect.bottom


def sendMsgToWX(msg, winname):
    try:
        hwnd = win32gui.FindWindow(qq_or_wx, winname)
        react = get_window_rect(hwnd)
        # win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
        try:
            win32gui.SetForegroundWindow(hwnd)
        except Exception as e:
            logger("请检查聊天窗口是否被覆盖")
            return False

        center_x = react[0] + int((react[2] - react[0]) / 2)
        center_y = react[3] - int((react[3] - react[1]) / 5)

        pyautogui.moveTo(center_x, center_y)

        if center_x < 0 or center_y < 0:
            raise Exception("该聊天窗口已被后台 请将聊天框置前并且那聊天窗口点击下光标")
        # print(center_x,center_y)
        # 将微信放在前台

        # 将鼠标移到(750, 700)
        pyautogui.moveTo(center_x, center_y)
        win32api.SetCursorPos((center_x, center_y))
        # 单击左键获取焦点
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, center_x, center_y, 0, 0)
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, center_x, center_y, 0, 0)

        # 将内容写入到粘贴板
        w.OpenClipboard()
        w.EmptyClipboard()
        w.SetClipboardData(win32con.CF_TEXT, msg.encode(encoding='gbk'))
        w.CloseClipboard()

        pyautogui.hotkey('ctrl', 'v')
        pyautogui.keyDown("enter")
        return True
    except Exception as e:
        logger("请确保该聊天窗口存在,异常信息:{}".format(e))
        return False


def main(winname):
    # totol_dic = set()
    # 接收内容
    l, res = spider()
    res = res
    for one in res:
        totol_dic.add(one)

    while 1:
        logger("检测新闻中")
        try:
            new_l, new_res = spider()
            if new_res:
                for one in new_res:
                    if one not in totol_dic:
                        one = time.strftime("%H:%M", time.localtime(time.time())) + " " + one + add_txt
                        for wn in winname:
                            if sendMsgToWX(one, wn):
                                logger("发送成功:{}".format(one))
                                totol_dic.add(one)
                            else:
                                logger("发送失败:{},下次将会重新发送".format(one))
                    else:
                        break
            time.sleep(sleep_time)
        except Exception as e:
            logger("运行错误.{}".format(e))


def test(winname):
    totol_dic = set()
    # 接收内容
    l, res = spider()
    res = res
    for one in res:
        one = one + add_txt
        if sendMsgToWX(one, winname):
            logger("发送成功:{}".format(one))
            time.sleep(2)
        else:
            loop = True
            while loop:
                if sendMsgToWX(one, winname):
                    loop = False
                logger("发送失败:{},下次将会重新发送".format(one))
                time.sleep(5)

        time.sleep(3)


if __name__ == '__main__':
    # test(winname)  #测试用
    # test(winname2)  #测试用
    logger("请将所有需要发送消息的窗口单独拖出来....")
    main(winname)  # 实际用

    # 测试多个窗口
    # for i in range(10):
    #     for one in winname:
    #         sendMsgToWX("测试"+str(i)+"", one)
