# @Time    : 2019/11/13 18:14
# @Author  : Libuda
# @FileName: 加密spider.py
# @Software: PyCharm
import json
import requests
import csv

"""
google搜索api
q:搜索关键词
cx:认证搜索引擎id
key:账户id
https://cse.google.com/cse/all
"""


class GoogleSpider(object):
    def __init__(self):
        self.url = "https://www.googleapis.com/customsearch/v1?key=xxx&q=2019%E5%A4%A7%E5%81%A5%E5%BA%B7%E8%AE%BA%E5%9D%9B&cx=xxxx&start={}&num=10&lr=lang_zh-CN"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        }
        self.li = []

    def get_page_from_url(self, url):
        """
        提取url
        :param url:
        :return:
        """
        html = requests.get(url, headers=self.headers).content
        # print(html)
        return html

    def get_data_from_page(self, page):
        """
        提取数据
        :param page:
        :return:
        """
        # print(page)
        if json.loads(page.decode())["items"]:
            data_list = json.loads(page.decode())["items"]
            return data_list
        else:
            print("no item")
            # print(len(data_list))

    def save_data(self, data_list):
        """
        保存数据
        :param data_list:
        :return:
        """
        for data in data_list:
            print(data)
            f = open('1.xls', 'w', encoding='utf-8-sig', newline='')
            writer = csv.writer(f)
            # 将一个个字段数据提取出来
            title = data['title']
            link = data['link']
            snippet = data['snippet']
            # print(title)
            t = (title, link, snippet)
            self.li.append(t)
            # 列表格式 ：[('xxxx',), ('xxxx',)]
            # print(self.li)
            # writerows保存多行，格式是[('xxxx',), ('xxxx',)] writerow保存单行，格式['a','b']
            writer.writerows(self.li)

    def run(self):
        i = 1
        while True:
            url = self.url.format(i)
            print(i)
            # 解析url
            page = self.get_page_from_url(url)
            # 获取+保存数据
            data_list = self.get_data_from_page(page)
            # 保存数据为csv
            self.save_data(data_list)
            if json.loads(page.decode())["queries"]["nextPage"]:
                i += 10
            else:
                break


if __name__ == '__main__':
    gg = GoogleSpider()
    gg.run()
