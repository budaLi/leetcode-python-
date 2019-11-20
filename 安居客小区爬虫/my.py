# @Time    : 2019/11/20 16:12
# @Author  : Libuda
# @FileName: my.py
# @Software: PyCharm
from selenium import webdriver
import pandas

new_house_file_path = r"C:\Users\lenovo\PycharmProjects\leetcode-python-\安居客小区爬虫\新房.xls"
ershou_file_path = r"C:\Users\lenovo\PycharmProjects\leetcode-python-\安居客小区爬虫\二手房.xls"
zufang_file_path = r'C:\Users\lenovo\PycharmProjects\leetcode-python-\安居客小区爬虫\租房.xls'
df = pandas.DataFrame()
chrome_options = webdriver.ChromeOptions()


def new_houser_spider():
    """
    新房爬虫
    :return:
    """
    global df
    new_house_page = 3  # 新房页数
    driver = webdriver.Chrome(chrome_options=chrome_options,
                              executable_path=r'C:\Users\lenovo\PycharmProjects\Spider\chromedriver.exe')
    houser_detail_url = "https://xn.fang.anjuke.com/loupan/canshu-{}.html?from=loupan_tab"  # 新房详情

    houser_url_lis = []
    for i in range(1, new_house_page + 1):
        new_houser_url = "https://xn.fang.anjuke.com/loupan/all/p{}/".format(str(i))
        driver.get(new_houser_url)
        links = driver.find_elements_by_css_selector(".item-mod")
        for link in links:
            houser_url_lis.append(link.get_attribute("data-link"))

    house_id_lis = []
    for house_url in houser_url_lis:
        if house_url:
            tem = house_url.split(".")[-2].split("/")[-1]
            house_id_lis.append(tem)

    print(house_id_lis)
    for house_id in house_id_lis:
        result = {}
        driver.get(houser_detail_url.format(house_id))
        try:
            house_name = driver.find_element_by_xpath(
                '//*[@id="container"]/div[1]/div[1]/div[1]/div[2]/ul/li[1]/div[2]/a').text  # 楼盘名称
            houser_leixing = driver.find_element_by_xpath(
                '//*[@id="container"]/div[1]/div[1]/div[3]/div[2]/ul/li[1]/div[2]').text.replace("[查看详情]", "")  #
            zhuangkuang = ""
            try:

                zhuangkuang = driver.find_element_by_xpath(
                    '//*[@id="container"]/div[1]/div[1]/div[3]/div[2]/ul/li[6]/div[2]').text  # 楼层状况
            except Exception as e:
                print("没有楼层状况")
            rongjilv = 0
            try:
                if driver.find_element_by_xpath(
                        '//*[@id="container"]/div[1]/div[1]/div[3]/div[2]/ul/li[3]/div[1]').text == "容积率":
                    rongjilv = driver.find_element_by_xpath(
                        '//*[@id="container"]/div[1]/div[1]/div[3]/div[2]/ul/li[3]/div[2]').text.replace("[查看详情]",
                                                                                                         "")  # 容积率
            except Exception:
                print("没有容积率")

            result['楼盘名称'] = house_name
            result['建筑类型'] = houser_leixing
            result['楼层状况'] = zhuangkuang
            result['容积率'] = rongjilv
            print(result)
            df = df.append([result])
            df.to_excel(new_house_file_path, index=0)
            print("已写入%s条" % str(len(df)))
        except Exception as e:
            print(e)
            continue


def EeShouHouser_spider():
    """
    二手房爬虫
    :return:
    """
    global df
    house_page = 3  # 页数
    driver = webdriver.Chrome(chrome_options=chrome_options,
                              executable_path=r'C:\Users\lenovo\PycharmProjects\Spider\chromedriver.exe')
    houser_detail_url = "https://xn.fang.anjuke.com/loupan/canshu-{}.html?from=loupan_tab"  # 新房详情

    houser_url_lis = []
    for i in range(1, house_page + 1):
        new_houser_url = "https://xining.anjuke.com/sale/p{}-y2/".format(str(i))  # y2表示2010后
        driver.get(new_houser_url)
        links = driver.find_elements_by_css_selector(".item-mod")
        for link in links:
            houser_url_lis.append(link.get_attribute("data-link"))

    house_id_lis = []
    for house_url in houser_url_lis:
        if house_url:
            tem = house_url.split(".")[-2].split("/")[-1]
            house_id_lis.append(tem)

    print(house_id_lis)
    for house_id in house_id_lis:
        result = {}
        driver.get(houser_detail_url.format(house_id))
        try:
            house_name = driver.find_element_by_xpath(
                '//*[@id="container"]/div[1]/div[1]/div[1]/div[2]/ul/li[1]/div[2]/a').text  # 楼盘名称
            houser_leixing = driver.find_element_by_xpath(
                '//*[@id="container"]/div[1]/div[1]/div[3]/div[2]/ul/li[1]/div[2]').text.replace("[查看详情]", "")  #
            zhuangkuang = ""
            try:

                zhuangkuang = driver.find_element_by_xpath(
                    '//*[@id="container"]/div[1]/div[1]/div[3]/div[2]/ul/li[6]/div[2]').text  # 楼层状况
            except Exception as e:
                print("没有楼层状况")
            rongjilv = 0
            try:
                if driver.find_element_by_xpath(
                        '//*[@id="container"]/div[1]/div[1]/div[3]/div[2]/ul/li[3]/div[1]').text == "容积率":
                    rongjilv = driver.find_element_by_xpath(
                        '//*[@id="container"]/div[1]/div[1]/div[3]/div[2]/ul/li[3]/div[2]').text.replace("[查看详情]",
                                                                                                         "")  # 容积率
            except Exception:
                print("没有容积率")

            result['楼盘名称'] = house_name
            result['建筑类型'] = houser_leixing
            result['楼层状况'] = zhuangkuang
            result['容积率'] = rongjilv
            print(result)
            df = df.append([result])
            df.to_excel(ershou_file_path, index=0)
            print("已写入%s条" % str(len(df)))
        except Exception as e:
            print(e)
            continue


def Zufang_spider():
    pass


if __name__ == '__main__':
    new_houser_spider()
