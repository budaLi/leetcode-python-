# @Time    : 2019/11/11 17:40
# @Author  : Libuda
# @FileName: ip.py
# @Software: PyCharm
# -*-coding:utf8-*-
# author : Lenovo
# date: 2018/8/17
import requests
from scrapy.selector import Selector
import MySQLdb

conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='root', db='crwal_ip', charset='utf8', use_unicode=True)
cursor = conn.cursor()


def crwal_xici_ip(random_ip=None):  # 爬ip     可以设置ip
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
    }
    ip_list = []
    proxy_dict = {}
    if random_ip:
        ip = random_ip.split(':')[0] + ':' + random_ip.split(':')[1]
        port = random_ip.split(':')[2]
        proxy_url = ip + port
        print(proxy_url)
        if random_ip.split(':')[0] == 'https':
            proxy_dict = {
                'https': proxy_url,  # 注意此处是http的ip
            }
        elif random_ip.split(':')[0] == 'http':
            proxy_dict = {
                'http': proxy_url,  # 注意此处是http的ip
            }
    for i in range(300, 1000):  # 提取3000页
        url = 'http://www.xicidaili.com/nn/{0}'.format(i)
        if proxy_dict:
            response = requests.get(url, headers=headers, proxies=proxy_dict)
        else:
            response = requests.get(url, headers=headers)
        if response.status_code == 200:
            selector = Selector(text=response.text)  # 可通过css xpath提取
            all_text = selector.css('#ip_list tr')[1:]  # 第一个为标题不需要
            for tr in all_text:  # 每一个tr下有多个td
                speed = tr.css('.bar::attr(title)').extract()[0]
                all_td = tr.css('td::text').extract()  # 全部td
                ip = all_td[0]
                port = all_td[1]
                type = all_td[5]
                ip_list.append((ip, port, type, speed))
            for one in ip_list:
                try:
                    sql = "insert ignore into crawl_ip(ip_url,port,ip_type,speed) VALUES('{0}','{1}','{2}','{3}')".format(
                        str(one[0]), str(one[1]), str(one[2]), str(one[3]))
                    cursor.execute(sql)
                    conn.commit()
                    print('可用ip:', (str(one[0]) + ':' + str(one[1])))
                except Exception as e:
                    pass


class GetIp(object):
    def get_random(self):  # 从数据库中随机获取ip
        result = cursor.execute(
            'select ip_url,port from crawl_ip order by rand() limit 1'
        )
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]
            if self.judge(ip, port):
                return 'https://{0}:{1}'.format(ip, port)
            else:
                return self.get_random()

    def judge(self, ip, port):  # 判断ip是否可以
        http_url = 'https://www.baidu.com'
        proxy_url = 'http://{0}:{1}'.format(ip, port)
        proxy_dict = {
            'http': proxy_url,  # 注意此处是http的ip
        }
        try:
            response = requests.get(http_url, proxies=proxy_dict)  # 使用指定ip
            print(response)
        except:
            print('此IP无效:{0}:{1}'.format(ip, port))
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if code >= 200 and code < 300:
                return True
            else:
                self.delete_ip(ip)
                print('此IP无效:{0}:{1}'.format(ip, port))
                return False

    def delete_ip(self, ip):  # 删除ip
        cursor.execute(
            'delete from crawl_ip where ip_url="{0}"'.format(ip)
        )
        conn.commit()
        return True


if __name__ == '__main__':
    # S=GetIp()       #取ip
    # print(S.get_random())
    # while 1:
    #     ip=S.get_random()
    #     print('当前使用ip:',ip)
    #     try:
    #         crwal_xici_ip(ip)   #爬i
    #     except:
    #         pass
    #     S.delete_ip(ip)     #爬玩不用了


    S = GetIp()
    while 1:
        res = S.get_random()
        print('此ip可用', res)
