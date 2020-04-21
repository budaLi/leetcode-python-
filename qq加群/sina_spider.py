# @Time    : 2020/4/21 9:49
# @Author  : Libuda
# @FileName: sina_spider.py
# @Software: PyCharm
import time
import requests


def sina_spider():
    to_res = []
    url = "http://zhibo.sina.com.cn/api/zhibo/feed?callback=jQuery111209796400473208458_1587433825027&page=1&page_size=20&zhibo_id=152&tag_id=5&dire=f&dpc=1&pagesize=20&id=1684365&type=0&_={}"
    _ = time.time() * 100

    response = requests.get(url.format(_)).text

    try:
        # print(len("try{jQuery111209796400473208458_1587433825027("))
        # print(len(");}catch(e){};"))
        response = eval(response[46:-14])
        res = response['result']['data']['feed']['list']
        for one in res:
            to_res.append(one['rich_text'])
        return 0, to_res

    except Exception as e:
        print(e)
        return 0, None
    # print(response)


if __name__ == '__main__':
    _, res = sina_spider()
    print(res)
