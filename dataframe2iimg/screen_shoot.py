# @Time    : 2020/6/9 16:37
# @Author  : Libuda
# @FileName: screen_shoot.py
# @Software: PyCharm
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium import webdriver
from PIL import Image
from datetime import datetime, time as dtime
import time

# 程序休眠时等待时间
time_sleep_totle = 300
# 截图时等待时间
time_sleep = 5
out_dir = "./out"


def logger(msg):
    """
    日志信息
    """
    now = time.ctime()
    print("[%s] %s" % (now, msg))


def main():
    logger("脚本开始执行")
    driver = webdriver.PhantomJS(executable_path="phantomjs.exe")
    driver.maximize_window()

    left, top, right, bottom = 632, 528, 1183, 1343
    driver.get("http://data.eastmoney.com/futures/sh/data.html?ex=069001005&va=RB")
    # 交易所选择
    jiaoyisuo_select = driver.find_element_by_id("futures_exchange")
    jiaoyisuo_options = Select(jiaoyisuo_select).options
    for i in range(len(jiaoyisuo_options)):
        logger("选择交易所:{}".format(jiaoyisuo_options[i].text))
        # 交易下拉框
        ActionChains(driver).move_to_element(jiaoyisuo_select).perform()
        Select(jiaoyisuo_select).select_by_index(i)

        # 选择品种
        pingzhong_select = driver.find_element_by_id("futures_variety")
        pingzhong_options = Select(pingzhong_select).options

        for j in range(len(pingzhong_options)):
            logger("选择品种:{}".format(pingzhong_options[j].text))
            ActionChains(driver).move_to_element(pingzhong_select).perform()
            Select(pingzhong_select).select_by_index(j)

            logger("当前交易所：{}，品种：{}".format(jiaoyisuo_options[i].text, pingzhong_options[j].text))
            # 点击查询
            driver.find_element_by_class_name("btn").click()
            time.sleep(time_sleep)
            driver.save_screenshot('capture.png')  # 截取全屏

            # ele1 = driver.find_element_by_xpath('//*[@id="mainContent"]/div[2]')
            # ele2 = driver.find_element_by_xpath('//*[@id="mainContent"]/div[7]')
            # 获取元素位置信息
            # left = ele1.location['x']-5
            # top = ele1.location['y']
            # right = left + ele1.size['width']*2+15
            # bottom = top + ele1.size['height']+ele2.size['height']+10
            # print(left,top,right,bottom)

            im = Image.open('capture.png')
            im = im.crop((left, top, right, bottom))  # 元素裁剪
            img_name = pingzhong_options[j].text + "持仓报告.png"
            im.save("./out/" + img_name)  # 元素截图

            # print("截图保存成功")
    driver.quit()


if __name__ == '__main__':

    DAY_START = dtime(21, 0)
    DAY_END = dtime(21, 20)

    NIGHT_START = dtime(21, 0)
    NIGHT_END = dtime(21, 20)

    while 1:
        t = time.gmtime()
        # 判断是否是星期天
        if t.tm_wday == 5 or t.tm_wday == 6:
            logger("星期天不执行脚本")
            time.sleep(time_sleep_totle)
            continue
        else:
            current_time = datetime.now().time()
            if DAY_START <= current_time <= DAY_END or (NIGHT_START <= current_time <= NIGHT_END):
                # 判断时候在可运行时间内
                logger("等待截图中")
                try:
                    main()
                    time.sleep(time_sleep_totle)
                except Exception as e:
                    print("运行错误", e)
                    time.sleep(time_sleep_totle)
            else:
                logger("其他时间段  其他任务执行中")
                time.sleep(time_sleep_totle)
