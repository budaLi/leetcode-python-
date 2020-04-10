# @Time    : 2019/11/14 8:37
# @Author  : Libuda
# @FileName: google_spider.py
# @Software: PyCharm
import sys

sys.path.append("./")
import time
from configparser import ConfigParser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

config_parser = ConfigParser()
config_parser.read('config.cfg')
config = config_parser['default']
wait_time = 0

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument(
    'user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')
chrome_options.add_argument('--no-sandbox')  # 这个配置很重要
browser = webdriver.Chrome(executable_path=config["executable_path"])
import xlrd
from xlutils.copy import copy  # 写入Excel

file_path = config['google_datas']

from operationExcel import OperationExcel


class Spider():
    def __init__(self):
        self.opExcel = OperationExcel(config['keywords_excel_path'], 0)
        self.dataExcel = OperationExcel(file_path, 0)

    def get_keywords_data(self, row):
        actual_data = OperationExcel(config['keywords_excel_path'], 0).get_cel_value(row, 0)
        return actual_data

    def write_to_excel(self, file_path, sheet_id, row, col, value):
        work_book = xlrd.open_workbook(file_path, formatting_info=False)
        # 先通过xlutils.copy下copy复制Excel
        write_to_work = copy(work_book)
        # 通过sheet_by_index没有write方法 而get_sheet有write方法
        sheet_data = write_to_work.get_sheet(sheet_id)
        sheet_data.write(row, col, str(value))
        # 这里要注意保存 可是会将原来的Excel覆盖 样式消失
        write_to_work.save(file_path)

    def main(self):

        # 打开登录页
        count = self.dataExcel.tables.nrows
        print("当前已有url数量：", count)
        tmp = count
        key_len = self.opExcel.get_nrows()
        print("关键词总数：", key_len)
        for index in range(key_len):
            key = self.get_keywords_data(index)

            try:
                browser.get("https://www.google.com/")
                time.sleep(wait_time)
                browser.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input').send_keys(key)
                time.sleep(wait_time)
                try:

                    browser.find_element_by_css_selector(
                        "#tsf > div:nth-child(2) > div.A8SBwf.emcav > div.UUbT9 > div.aajZCb > div.tfB0Bf > center > input.gNO89b").click()
                except:
                    browser.find_element_by_css_selector(
                        "#tsf > div:nth-child(2) > div.A8SBwf > div.FPdoLc.tfB0Bf > center > input.gNO89b").click()
            except Exception as e:
                print(e)
                browser.get("https://www.google.com/")
                time.sleep(wait_time)
                browser.find_element_by_css_selector(
                    "#tsf > div:nth-child(2) > div.A8SBwf > div.RNNXgb > div > div.a4bIc > input").send_keys(key)
                time.sleep(wait_time)
                browser.find_element_by_css_selector(
                    "#tsf > div:nth-child(2) > div.A8SBwf.emcav > div.UUbT9 > div.aajZCb > div.tfB0Bf > center > input.gNO89b").click()

            res_set = set()
            page = 1
            flag = True
            while flag:

                try:
                    print("当前正在采集第 {} 个关键词:{}，采集的页数为 :{} ".format((index + 1), key, page))
                    page += 1
                    time.sleep(wait_time)
                    title = browser.find_elements_by_css_selector(".LC20lb")
                    url = browser.find_elements_by_xpath('//*[@class="r"]/a')
                    for i in range(len(title)):
                        s = url[i].get_attribute("href").split("/")
                        try:
                            tmp = s[0] + "//" + s[2]
                        except Exception as e:
                            print("url解析错误", s)
                            tmp = s[0] + "//" + s[2]

                        if tmp not in res_set and title[i].text != "":
                            res_set.add(tmp)
                            try:
                                self.write_to_excel(file_path, 0, count, 0, title[i].text)
                                self.write_to_excel(file_path, 0, count, 1, tmp)
                                print(count, title[i].text, tmp)
                                count += 1
                            except Exception as e:
                                print(e, "请关闭Excel 否则10秒后本条数据将不再写入")
                                for i in range(10):
                                    print(10 - i)
                                    time.sleep(1)
                                try:
                                    self.write_to_excel(file_path, -1, count, 0, title[i].text)
                                    self.write_to_excel(file_path, -1, count, 1, tmp)
                                    print(count, title[i].text, tmp, browser.current_url)
                                except Exception:
                                    print("已漏掉数据...{}  {}".format(title[i].text, tmp))

                    next_paget = browser.find_element_by_css_selector("#pnnext > span:nth-child(2)")
                    next_paget.click()
                    # print("点击下一页")
                    time.sleep(wait_time)
                except Exception as e:
                    try:
                        browser.find_element_by_css_selector("#pnnext > span:nth-child(2)")
                        continue
                    except Exception as e:

                        print("已经是最后一页")
                        try:
                            if browser.find_element_by_xpath("/html/body/div[1]/div/b").text == "关于此网页":
                                print("遇到反爬验证码")
                                return False
                        except Exception:
                            break

                        # switch = input("是否已切换ip并继续爬取下个关键字？")
                        # if switch == "y":
                        #     break
                        # else:
                        #     print("请您切换ip")
        # print("本次采集已获取url总数为：", str(count-tmp))
        print("关键词搜索完毕，谢谢使用!")
        while 1:
            pass


if __name__ == "__main__":
    print("欢迎使用 （谷歌搜索引擎爬虫）")
    while 1:
        spider = Spider()
        if not spider.main():
            continue
