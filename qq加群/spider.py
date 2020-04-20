# @Time    : 2020/3/23 11:20
# @Author  : Libuda
# @FileName: spider.py
# @Software: PyCharm
import requests
import time

base_url = "https://newsapi.eastmoney.com/kuaixun/v1/getlist_106_ajaxResult_50_1_.html?&_={}"


def spider():
    try:
        res = []
        url = base_url.format(int(time.time() * 1000))
        response = requests.get(url).text
        totle_res = eval(response.replace("var ajaxResult=", ""))
        lis_res = totle_res['LivesList'][:20]
        for one in lis_res:
            res.append(one['digest'].replace("</b>", ""))
        return (len(lis_res), res)
    except Exception as e:
        return (0, None)


def main():
    lenght, res = spider()
    if lenght != 0:
        return res


if __name__ == '__main__':

    l, res = spider()
    print("{}:{}".format(time.ctime(), res))
    # time.sleep(600)

    while 1:
        new_l, new_res = spider()
        if res != new_res:
            print("{}:{}".format(time.ctime(), new_res))
            res = new_res
        else:
            print("{},新闻：{}".format(time.ctime(), l))
        time.sleep(300)
