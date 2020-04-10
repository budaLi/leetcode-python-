# @Author  : Libuda
# @FileName: google_spider.py
# @Software: PyCharm
import sys

sys.path.append("./")
from configparser import ConfigParser
from selenium import webdriver
import time
import xlrd
import base64
from queue import Queue
from xlutils.copy import copy  # 写入Excel

config_parser = ConfigParser()
config_parser.read('config.cfg')
config = config_parser['default']
browser = webdriver.PhantomJS(executable_path=config['executable_path'])

from operationExcel import OperationExcel

res_count = 0


class Spider():
    def __init__(self):
        self.opExcel = OperationExcel(config['keywords_excel_path'], 0)
        self.file_path = config['biying_datas']
        # self.pass_key_excel = OperationExcel(config['pass_key_path'],0)
        self.dataExcel = OperationExcel(self.file_path, 0)
        self.keywords_queue = Queue()
        self.res = set()

    def get_keywords_data(self, row):
        """
        获取关键词数据
        :param row:
        :return:
        """
        actual_data = OperationExcel(config['keywords_excel_path'], 0).get_cel_value(row, 0)
        return actual_data

    def write_to_excel(self, file_path, sheet_id, row, col, value):
        """
        写入Excel
        :param sheet_id:
        :param row:
        :param col:
        :param value:
        :return:
        """
        work_book = xlrd.open_workbook(file_path, formatting_info=False)
        # 先通过xlutils.copy下copy复制Excel
        write_to_work = copy(work_book)
        # 通过sheet_by_index没有write方法 而get_sheet有write方法
        sheet_data = write_to_work.get_sheet(sheet_id)
        sheet_data.write(row, col, str(value))
        # 这里要注意保存 可是会将原来的Excel覆盖 样式消失
        write_to_work.save(file_path)

    def main(self):
        global res_count
        test_count = int(config['max_test_count'])
        last_count = 0
        count = self.dataExcel.tables.nrows
        print("当前已有url数量：", count)
        key_len = self.opExcel.get_nrows()
        print("关键词总数：", key_len)
        # tem = 0 if self.pass_key_excel.tables.nrows==0 else self.pass_key_excel.tables.nrows-1
        # print("已爬取关键词个数 :",tem)
        # print("剩余爬取关键词个数:",key_len-tem)
        for index in range(1, key_len):

            key = self.get_keywords_data(index)

            try:
                print("启动中。。。。，如果20s内没有启动 请重新启动本软件")
                browser.get("https://cn.bing.com/?FORM=BEHPTB&ensearch=1")
                browser.find_element_by_css_selector("#sb_form_q").send_keys(key)
                browser.find_element_by_css_selector("#sb_form_go").click()

                for i in range(20):
                    if browser.current_url != "https://cn.bing.com/?FORM=BEHPTB&ensearch=1":
                        continue
                    else:
                        print(20 - i)
                        time.sleep(1)
                        print("正在第{}次尝试自动启动。。。。。".format(i + 1))
                        browser.get("https://cn.bing.com/?FORM=BEHPTB&ensearch=1")
                        browser.find_element_by_css_selector("#sb_form_q").send_keys(key)
                        browser.find_element_by_css_selector("#sb_form_go").click()
            except Exception as e:
                # print(e)
                print("正在尝试自动启动。。。。。")
                browser.get("https://cn.bing.com/?FORM=BEHPTB&ensearch=1")
                browser.find_element_by_css_selector("#sb_form_q").send_keys(key)
                browser.find_element_by_css_selector("#sb_form_go").click()

            current_url_set = set()
            flag = True
            while flag:
                try:
                    if browser.current_url in current_url_set:
                        if test_count < 0:
                            print("no next")
                            flag = False
                        else:
                            print("当前url {} 可能为最后一页,进行第{}次测试".format(browser.current_url, test_count))
                            test_count -= 1
                    else:
                        print("当前正在采集第 {} 个关键词:{}，采集的页数为 :{} ".format((index + 1), key, len(current_url_set) + 1))
                        print("当前url", browser.current_url)
                        current_url_set.add(browser.current_url)

                    title = browser.find_elements_by_css_selector("#b_results > li > h2")
                    url = browser.find_elements_by_css_selector('#b_results > li> h2 > a')
                    for i in range(len(url)):

                        s = url[i].get_attribute("href").split("/")
                        try:
                            tmp = s[0] + "//" + s[2]
                        except Exception as e:
                            # print(e)
                            tmp = s[0] + "//" + s[2]
                        if tmp not in self.res:
                            self.res.add(tmp)
                            try:
                                self.write_to_excel(self.file_path, -1, count, 0, title[i].text)
                                self.write_to_excel(self.file_path, -1, count, 1, tmp)
                                print(count, title[i].text, tmp)
                                count += 1
                                res_count += 1
                            except Exception as e:
                                print(e, "请关闭Excel 否则10秒后本条数据将不再写入")
                                for i in range(10):
                                    print(10 - i)
                                    time.sleep(1)
                                try:
                                    self.write_to_excel(self.file_path, -1, count, 0, title[i].text)
                                    self.write_to_excel(self.file_path, -1, count, 1, tmp)
                                    print(count, title[i].text, tmp, browser.current_url)
                                except Exception:
                                    print("已漏掉数据...{}  {}".format(title[i].text, tmp))

                    try:
                        next_paget = browser.find_element_by_css_selector(
                            "#b_results > li.b_pag > nav > ul > li:nth-child(9) > a")
                        next_paget.click()
                    except Exception as e:
                        # print(e)
                        try:
                            next_paget = browser.find_element_by_css_selector(
                                "#b_results > li.b_pag > nav > ul > li:nth-child(8) > a")
                            next_paget.click()
                        except Exception as e:
                            # print(e)
                            next_paget = browser.find_element_by_css_selector(
                                "#b_results > li.b_pag > nav > ul > li:nth-child(7) > a")
                            next_paget.click()
                except Exception as e:
                    # print(e)
                    try:
                        try:
                            next_paget = browser.find_element_by_css_selector(
                                "#b_results > li.b_pag > nav > ul > li:nth-child(9) > a")
                            next_paget.click()
                        except Exception as e:
                            # print(e)
                            try:
                                next_paget = browser.find_element_by_css_selector(
                                    "#b_results > li.b_pag > nav > ul > li:nth-child(8) > a")
                                next_paget.click()
                            except Exception as e:
                                try:
                                    next_paget = browser.find_element_by_css_selector(
                                        "#b_results > li.b_pag > nav > ul > li:nth-child(7) > a")
                                    next_paget.click()
                                except Exception as e:
                                    # print(e)
                                    try:
                                        next_paget = browser.find_element_by_css_selector(
                                            "#b_results > li.b_pag > nav > ul > li:nth-child(6) > a")
                                        next_paget.click()
                                    except Exception as e:
                                        print("找不到下一页呢")
                                        time.sleep(5)
                                        flag = False
                    except Exception as e:
                        print(e)
                        print("可能是最后一页了呢 当前url为{}".format(browser.current_url))
                        time.sleep(5)
                        flag = False

            try:
                # self.write_to_excel(config['pass_key_path'],0,tem,0,key)
                # self.write_to_excel(config['pass_key_path'],0,tem,1,res_count-last_count)
                print("当前关键词 ：{} 爬取完毕 已爬取数据 ：{}".format(key, res_count - last_count))
            except Exception as e:
                print(e)

            print("本次采集已获取url总数为：", str(res_count))
            last_count = res_count
        print("关键词搜索完毕，谢谢使用!")
        while 1:
            pass


if __name__ == "__main__":
    spider = Spider()
    spider.main()
