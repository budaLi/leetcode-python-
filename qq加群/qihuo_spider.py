# @Time    : 2020/4/15 18:29
# @Author  : Libuda
# @FileName: qihuo_spider.py
# @Software: PyCharm

import requests


def spider():
    url = "https://flash-api.jin10.com/get_flash_list?channel=2"
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        # 'cookie': 'UM_distinctid=1717d593c7d74c-0998a4179c093a-5313f6f-144000-1717d593c7e5bc; x-token=',
        'origin': 'https://www.jin10.com',
        'referer': 'https://www.jin10.com/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
        'x-app-id': 'SO1EJGmNgCtmpcPF',
        'x-version': '1.0.0',
    }
    response = requests.get(url, headers=headers).json()

    res = []
    for i in range(10):
        tem = response['data'][i]['data']['content']
        if "现货报价" in tem or "了解请戳" in tem:
            continue
        tem = tem.replace("金十期货讯", "").replace("。", "。/n/n").replace("<b>", "")
        res.append(tem)

    return 0, res


if __name__ == '__main__':
    res = spider()
    print(res)
