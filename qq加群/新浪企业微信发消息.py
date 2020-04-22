# @Time    : 2020/4/4 17:13
# @Author  : Libuda
# @FileName: 企业微信发消息.py
# @Software: PyCharm
import win32gui
import win32api
import win32con
import win32clipboard as w
import win32clipboard
import time
import ctypes
import pyautogui
from datetime import datetime
from datetime import time as dtime
import smtplib  # 发送邮件 连接邮件服务器
from email.mime.text import MIMEText  # 构建邮件格式
from fake_useragent import UserAgent

from qq加群.sina_spider import sina_spider

#  安全限制
pyautogui.FAILSAFE = False

# qq_or_wx = "TXGuiFoundation"  qq
qq_or_wx = "ChatWnd"  # 微信
# qq_or_wx = "WwStandaloneConversationWnd"  # 企业微信
sleep_time = 120
send_message_count = 10  # 每隔多长时间发送一次联系人微信
# 休眠时间
winname = ["Q"]  # 需要发送的
wx_number = {"Q": [1, "李不搭", "15735656005"],
             "期货快讯1088群": [1088, "小祝", "876134889"],
             "快讯3088群@孺子牛": [3088, "孺子牛", "13699679997"],
             }  # 不同群对应发送的微信号
add_txt = "\n \n 各位朋友好，欢迎来到实时期货快讯{}群，我是{}，我的微信号是：{}，欢迎大家一起交流。"
user_list = ['1364826576@qq.com', "1410000000@qq.com"]  # 给谁发邮件
log_path = "log.txt"  #日志信息
totol_dic = set()  # 去重

l, res = sina_spider()

for one in res[1:]:
    totol_dic.add(one)


class SendEmail:
    def __init__(self):
        # 发件人
        self.send_user = "李晋军" + "<1364826576@qq.com>"
        # 登录名
        self.login_user = '1364826576@qq.com'
        # 这里要注意 不是qq密码 而是在邮箱里设置的发送邮箱的授权码
        self.password = 'btfixrcdeguejfja'
        # 发送邮件的服务器地址 qq为smtp.qq.com  163邮箱为smtp.163.com
        self.email_host = 'smtp.qq.com'

    def send_email(self, userlist, subject, content):
        message = MIMEText(content, _subtype='plain', _charset='utf-8')
        message['Subject'] = subject
        message['From'] = self.send_user
        message['To'] = ';'.join(userlist)  # 收件人列表以分号隔开
        # 实例化邮件发送服务器
        server = smtplib.SMTP()
        # 连接qq邮箱服务器
        server.connect(self.email_host)
        # 登录服务器
        server.login(self.login_user, self.password)
        # 发送邮件  注意此处消息的格式应该用as_string()函数
        server.sendmail(self.send_user, userlist, message.as_string())
        # 关闭邮箱
        server.close()

    def send_test(self, userlist, passNumber, failNumber):
        """
        发送测试结果
        :param userlist:
        :param passNumber:
        :param failNumber:
        :return:
        """
        totalNumber = passNumber + failNumber

        # %.2f表示保留小数点后两位小数 %%表示百分之百
        passPercentage = "%.2f%%" % (passNumber / totalNumber * 100)
        failPercentae = "%.2f%%" % (failNumber / totalNumber * 100)

        sub = "测试结果报告"
        content = " 测试用例总数\t%s个\n通过个数\t%s个\n失败个数\t%s个\n通过率\t%s\n失败率\t%s" % (
            totalNumber, passNumber, failNumber, passPercentage, failPercentae)
        self.send_email(userlist, sub, content)
        return True

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
    send_em = SendEmail()
    count = 0
    global totol_dic
    while 1:
        current_time = datetime.now().time()

        DAY_START = dtime(8, 0)
        DAY_END = dtime(12, 0)

        NIGHT_START = dtime(13, 0)
        NIGHT_END = dtime(20, 0)

        if DAY_START <= current_time <= DAY_END or (NIGHT_START <= current_time <= NIGHT_END):
            logger("检测新闻中")
            try:
                l, new_res = sina_spider()

                if new_res:
                    logger(new_res)
                    for one in new_res:
                        if one not in totol_dic:
                            count += 1
                            if count % send_message_count == 0:
                                tem = time.strftime("%H:%M", time.localtime(time.time())) + " " + one + add_txt
                            else:
                                tem = time.strftime("%H:%M", time.localtime(time.time())) + " " + one
                            for wn in winname:
                                s = tem
                                s = s.format(*wx_number[wn])
                                if sendMsgToWX(s, wn):
                                    logger("发送成功:{}".format(s))
                                    totol_dic.add(one)
                                    with open(log_path, 'a') as f:
                                        now = time.ctime()
                                        content = "[%s] %s" % (now, s)
                                        f.write(content)
                                        f.write("\n")
                                    send_em.send_email(user_list, "新浪信号发送成功通知", "信息为：{}".format(s))
                                else:
                                    flag = 3
                                    while flag > 0:
                                        if sendMsgToWX(s, wn):
                                            flag = 0
                                            logger("发送成功:{}".format(s))
                                            totol_dic.add(one)
                                            with open(log_path, 'a') as f:
                                                now = time.ctime()
                                                content = "[%s] %s" % (now, s)
                                                f.write(content)
                                                f.write("\n")
                                            send_em.send_email(user_list, "新浪信号发送成功通知", "信息为：{}".format(s))
                                        else:
                                            flag -= 1
                                            with open(log_path, 'a') as f:
                                                now = time.ctime()
                                                content = "[%s] %s" % (now, s + "发送失败！")
                                                f.write(content)
                                                f.write("\n")
                        # else:
                        #     break

                else:
                    logger("可能被反爬导致无数据：{}".format(new_res))

            except Exception as e:
                logger("运行错误.{}".format(e))
                with open(log_path, 'a') as f:
                    now = time.ctime()
                    content = "[%s] %s" % (now, e)
                    f.write(content)
                    f.write("\n")
                send_em.send_email(user_list, "新浪发微信程序异常", "异常信息为：{}".format(e))

        else:
            logger("不在时间段")

        time.sleep(sleep_time)

if __name__ == '__main__':

    logger("请将所有需要发送消息的窗口单独拖出来....")

    # 断网或者其他未知错误捕获 写入日志 发送邮件
    while 1:
        try:
            main(winname)  # 实际用
        except Exception as e:
            logger("运行错误.{}".format(e))
            with open(log_path, 'a') as f:
                now = time.ctime()
                content = "[%s] %s" % (now, e)
                f.write(content)
                f.write("\n")
            send_em = SendEmail()
            send_em.send_email(user_list, "新浪发微信程序异常", "异常信息为：{}".format(e))
            time.sleep(60)
