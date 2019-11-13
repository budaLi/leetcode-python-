# @Time    : 2019/11/11 13:29
# @Author  : Libuda
# @FileName: baidu.py
# @Software: PyCharm
# coding:utf-8
import requests
import os
import re
import itertools
import urllib
import sys
import urllib.request as urllib2
import io
from  PIL import Image
from queue import Queue
from ip import GetIp
import threading

count = 0
max_size = 100
url_queue = Queue()
image_queue = Queue(max_size)
index_queue = Queue()
str_table = {
    '_z2C$q': ':',
    '_z&e3B': '.',
    'AzdH3F': '/'
}

char_table = {
    'w': 'a',
    'k': 'b',
    'v': 'c',
    '1': 'd',
    'j': 'e',
    'u': 'f',
    '2': 'g',
    'i': 'h',
    't': 'i',
    '3': 'j',
    'h': 'k',
    's': 'l',
    '4': 'm',
    'g': 'n',
    '5': 'o',
    'r': 'p',
    'q': 'q',
    '6': 'r',
    'f': 's',
    'p': 't',
    '7': 'u',
    'e': 'v',
    'o': 'w',
    '8': '1',
    'd': '2',
    'n': '3',
    '9': '4',
    'c': '5',
    'm': '6',
    '0': '7',
    'b': '8',
    'l': '9',
    'a': '0'
}
char_table = {ord(key): ord(value) for key, value in char_table.items()}


# 解码
def decode(url):
    for key, value in str_table.items():
        url = url.replace(key, value)
    return url.translate(char_table)


# 百度图片下拉
def buildUrls(word):
    word = urllib.parse.quote(word)
    url = r"http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&fp=result&queryWord={word}&cl=2&lm=-1&ie=utf-8&oe=utf-8&st=-1&ic=0&word={word}&face=0&istype=2nc=1&pn={pn}&rn=60"
    urls = (url.format(word=word, pn=x) for x in itertools.count(start=0, step=60))

    return urls


re_url = re.compile(r'"objURL":"(.*?)"')


# 获取imgURL
def resolveImgUrl(html):
    # imgUrls = [decode(x) for x in re_url.findall(html)]
    # return imgUrls
    for i, x in enumerate(re_url.findall(html)):
        image_queue.put(decode(x))


def check_image_size(image_url):
    try:
        file = urllib2.urlopen(image_url)
        tmpIm = io.BytesIO(file.read())
        im = Image.open(tmpIm)
        if im.size[0] <= 256 or im.size[1] <= 256 or (im.size[0] == 360 and im.size[1] == 360):
            return False
        else:
            return True
    except Exception as e:
        return False


# 下载图片
def downImgs(imgUrl, dirpath, imgName, imgType, proxy_dict=None):
    global count
    filename = os.path.join(dirpath, imgName)
    try:
        res = requests.get(url=imgUrl, timeout=15)
        if str(res.status_code)[0] == '4':
            print(str(res.status_code), ":", imgUrl)
            return False
    except Exception as e:
        print('抛出异常:', imgUrl)
        print(e)
        return False
    with open(filename + '.' + imgType, 'wb') as f:
        f.write(res.content)
        count += 1
    return True


# 创建文件路径
def mkDir(dirName):
    dirpath = os.path.join(sys.path[0], dirName)
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    return dirpath


def main(proxies):
    while not image_queue.empty():
        image_url = image_queue.get(timeout=10)
        if check_image_size(image_url):
            downImgs(image_url, dirpath, index_queue.get() + ".jpg", imgType, proxies)


if __name__ == '__main__':
    getip = GetIp()
    lis = ["菊花粥"]
    for i in range(0, 100000):
        index_queue.put(str(i))
    for one in lis:
        ip = getip.get_random()
        print("当前使用ip", ip)
        path = one
        dirpath = mkDir(path)
        word = one
        imgType = 'jpg'
        strtag = imgType
        urls = buildUrls(word)
        index = 0
        for url in urls:
            if count > 1600:
                count = 0
                break
            print("正在请求：", url)
            proxy_dict = {
                'https': ip,  # 注意此处是http的ip
            }
            html = requests.get(url, timeout=10, proxies=proxy_dict).content.decode('utf-8')
            resolveImgUrl(html)
            downloads = []
            for i in range(100):
                download = threading.Thread(target=main, args=(proxy_dict,))
                downloads.append(download)

            for one in downloads:
                one.start()
            for one in downloads:
                one.join()
