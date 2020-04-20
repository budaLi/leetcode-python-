# @Author  : Libuda
# @FileName: google_spider.py
# @Software: PyCharm
import sys

sys.path.append("./")
from configparser import ConfigParser
from selenium import webdriver
import time
import xlrd
from xlutils.copy import copy as xl_copy
import base64
from queue import Queue

config_parser = ConfigParser()
config_parser.read('config.cfg')
config = config_parser['default']

browser = webdriver.PhantomJS(executable_path=config['executable_path'])


res_count = 0


def logger(msg):
    """
    日志信息
    """
    # now = time.ctime()
    print("%s" % (msg))


class OperationExcel():
    """
    #以面向对象的方式操作Excel
    """

    def __init__(self, file_name=None, sheet_id=None):
        """
        初始化OperationExcel对象
        :param file_name:
        :param sheet_id: vv
        """
        if file_name:
            self.file_name = file_name
            self.sheet_id = sheet_id
        else:
            self.file_name = r"C:\Users\lenovo\PycharmProjects\Spider\biying_data.xls"
            self.sheet_id = 0
        self.tables = self.get_tables()

    def create_sheet(self, sheet_name):
        ecel = xlrd.open_workbook(self.file_name)
        wb = xl_copy(ecel)
        wb.add_sheet(sheet_name)
        wb.save(self.file_name)

    def get_tables(self):
        """
        返回tables对象
        :return:
        """
        ecel = xlrd.open_workbook(self.file_name)
        tables = ecel.sheet_by_index(self.sheet_id)
        return tables

    def get_nrows(self):
        """
        获取表格行数
        :return:
        """
        return self.tables.nrows

    def get_ncols(self):
        """
        获取表格列数
        :return:
        """
        return self.tables.ncols

    def get_data_by_row(self, row):
        """
        根据行号获取某一行的内容
        :param row:
        :return:
        """
        if row < 0:
            row = 0
        if row > self.get_nrows():
            row = self.get_nrows()
        data = self.tables.row_values(row)
        return data

    def get_data_by_col(self, col):
        """
        根据列号返回某一列的内容
        :param col:
        :return:
        """
        if col < 0:
            col = 0
        if col > self.get_ncols():
            col = self.get_ncols()
        data = self.tables.col_values(col)
        return data

    def get_cel_value(self, row, col):
        """
        获取某个指定单元格的内容
        :param row:
        :param col:
        :return:
        """
        data = self.tables.cell_value(row, col)

        # ecxel中读取数据时默认将数字类型读取为浮点型
        if isinstance(data, float):
            data = int(data)
        return data

class Spider():
    def __init__(self):
        self.opExcel = OperationExcel(config['keywords_excel_path'], 0)
        self.file_path = config['biying_datas']
        self.title_fillter = config['title_fillter'].split(",")
        self.url_fillter = config['url_fillter'].split(",")
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
        write_to_work = xl_copy(work_book)
        # 通过sheet_by_index没有write方法 而get_sheet有write方法
        sheet_data = write_to_work.get_sheet(sheet_id)
        sheet_data.write(row, col, str(value))
        # 这里要注意保存 可是会将原来的Excel覆盖 样式消失
        write_to_work.save(file_path)

    def main(self):
        global res_count
        start_index = int(config['start_index'])
        last_count = 0
        count = self.dataExcel.tables.nrows
        logger("当前已有url数量：{}".format(count))
        key_len = self.opExcel.get_nrows()
        logger("关键词总数：{}".format(key_len))
        # tem = 0 if self.pass_key_excel.tables.nrows==0 else self.pass_key_excel.tables.nrows-1
        # logger("已爬取关键词个数 :",tem)
        # logger("剩余爬取关键词个数:",key_len-tem)
        for index in range(start_index, key_len):
            test_count = int(config['max_test_count'])
            key = self.get_keywords_data(index)

            try:
                logger("启动中。。。。如果20s内没有启动 请重新启动本软件")
                browser.get("https://cn.bing.com/?FORM=BEHPTB&ensearch=1")
                browser.find_element_by_css_selector("#sb_form_q").send_keys(key)
                browser.find_element_by_css_selector("#sb_form_go").click()

                for i in range(20):
                    if browser.current_url != "https://cn.bing.com/?FORM=BEHPTB&ensearch=1":
                        continue
                    else:
                        logger(20 - i)
                        time.sleep(1)
                        logger("正在第{}次尝试自动启动。。。。。".format(i + 1))
                        browser.get("https://cn.bing.com/?FORM=BEHPTB&ensearch=1")
                        browser.find_element_by_css_selector("#sb_form_q").send_keys(key)
                        browser.find_element_by_css_selector("#sb_form_go").click()
            except Exception as e:
                # logger(e)
                logger("正在尝试自动启动。。。。。")
                browser.get("https://cn.bing.com/?FORM=BEHPTB&ensearch=1")
                browser.find_element_by_css_selector("#sb_form_q").send_keys(key)
                browser.find_element_by_css_selector("#sb_form_go").click()

            current_url_set = set()
            flag = True
            while flag:
                try:
                    if browser.current_url in current_url_set:
                        if test_count < 0:
                            logger("no next")
                            flag = False
                        else:
                            logger("当前url {} 可能为最后一页,进行第{}次测试".format(browser.current_url, test_count))
                            test_count -= 1
                    else:
                        logger("当前正在采集第 {} 个关键词:{}，采集的页数为 :{} ".format((index + 1), key, len(current_url_set) + 1))
                        logger("当前url:{}".format(browser.current_url))
                        current_url_set.add(browser.current_url)

                    title = browser.find_elements_by_css_selector("#b_results > li > h2 ")
                    url = browser.find_elements_by_css_selector('#b_results > li > h2 > a')

                    for i in range(len(url)):

                        s = url[i].get_attribute("href").split("/")
                        try:
                            tmp = s[0] + "//" + s[2]
                        except Exception as e:
                            # logger(e)
                            tmp = s[0] + "//" + s[2]

                        pass_flag = False
                        for one in self.url_fillter:
                            if one in tmp:
                                pass_flag = True
                        for one in self.title_fillter:
                            if one in title[i].text:
                                pass_flag = True

                        if not pass_flag and tmp not in self.res:
                            self.res.add(tmp)
                            try:
                                self.write_to_excel(self.file_path, -1, count, 0, title[i].text)
                                self.write_to_excel(self.file_path, -1, count, 1, tmp)
                                logger("{},{},{}".format(count, title[i].text, tmp))
                                count += 1
                                res_count += 1
                            except Exception as e:
                                logger("请关闭Excel 否则10秒后本条数据将不再写入：{}".format(e))
                                for i in range(10):
                                    logger(10 - i)
                                    time.sleep(1)
                                try:
                                    self.write_to_excel(self.file_path, -1, count, 0, title[i].text)
                                    self.write_to_excel(self.file_path, -1, count, 1, tmp)
                                    logger("{},{},{},{}".format(count, title[i].text, tmp, browser.current_url))
                                except Exception:
                                    logger("已漏掉数据...{}  {}".format(title[i].text, tmp))

                    try:
                        next_paget = browser.find_element_by_css_selector(
                            "#b_results > li.b_pag > nav > ul > li:nth-child(9) > a")
                        next_paget.click()
                    except Exception as e:
                        # logger(e)
                        try:
                            next_paget = browser.find_element_by_css_selector(
                                "#b_results > li.b_pag > nav > ul > li:nth-child(8) > a")
                            next_paget.click()
                        except Exception as e:
                            # logger(e)
                            next_paget = browser.find_element_by_css_selector(
                                "#b_results > li.b_pag > nav > ul > li:nth-child(7) > a")
                            next_paget.click()
                except Exception as e:
                    # logger(e)
                    try:
                        try:
                            next_paget = browser.find_element_by_css_selector(
                                "#b_results > li.b_pag > nav > ul > li:nth-child(9) > a")
                            next_paget.click()
                        except Exception as e:
                            # logger(e)
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
                                    # logger(e)
                                    try:
                                        next_paget = browser.find_element_by_css_selector(
                                            "#b_results > li.b_pag > nav > ul > li:nth-child(6) > a")
                                        next_paget.click()
                                    except Exception as e:
                                        logger("找不到下一页呢")
                                        time.sleep(5)
                                        flag = False
                    except Exception as e:
                        logger(e)
                        logger("可能是最后一页了呢 当前url为{}".format(browser.current_url))
                        time.sleep(5)
                        flag = False

            try:
                # self.write_to_excel(config['pass_key_path'],0,tem,0,key)
                # self.write_to_excel(config['pass_key_path'],0,tem,1,res_count-last_count)
                logger("当前关键词 ：{} 爬取完毕 已爬取数据 ：{}".format(key, res_count - last_count))
            except Exception as e:
                logger(e)

            logger("本次采集已获取url总数为：{}".format(str(res_count)))
            last_count = res_count
            start_index += 1
            config_parser.set("default", "start_index", str(start_index))
            config_parser.write(open("config.cfg", 'w'))

        logger("关键词搜索完毕，谢谢使用!")
        while 1:
            pass


if __name__ == "__main__":

    try:
        code = config['code']
        now_time = int(time.time())
        s = str(base64.b64decode(code), "utf-8")
        s2 = time.strptime(s, "%Y-%m-%d %H:%M:%S")
        time_sti = int(time.mktime(s2))  # 时间戳
        if now_time > time_sti:
            logger("您的注册码已过期")
            time.sleep(10)
        else:
            logger("欢迎使用 国外搜索系统")
            logger("软件将于  '{}'    过期  ".format(s))
            spider = Spider()
            spider.main()
    except Exception as e:
        logger("您的使用权限已过期")
        time.sleep(10)
