# @Time    : 2019/12/18 18:17
# @Author  : Libuda
# @FileName: 远程服务器文件监控.py
# @Software: PyCharm
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Length': '58',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'JSESSIONID=BB4fd57DyY3xJK9ShNTlZGFjvQm86Gp8TWG5jkhlCQTPWht17Kjz!-1068374446; BIGipServerweb_pool=2113995018.36895.0000',
    'Host': 'www1.nm.zsks.cn',
    'Origin': 'https://www1.nm.zsks.cn',
    'Referer': 'https://www1.nm.zsks.cn/xxcx/gkcx/lqmaxmin_19.jsp',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",
    'cookies': "JSESSIONID=BB4fd57DyY3xJK9ShNTlZGFjvQm86Gp8TWG5jkhlCQTPWht17Kjz!-1068374446; BIGipServerweb_pool=2113995018.36895.0000"
}
import requests
from bs4 import BeautifulSoup

tem_data = """1 本科提前A
2 本科提前B
3 本科一批
4 本科二批
6 专科提前
7 高职高专
9 高职扩招
C 本科一批B
E 本科二批B
@ 汉授编导
A 普通文科
B 普通理科
C 蒙授文科
D 蒙授理科
E 汉授美术
F 蒙授美术
G 汉授音乐
H 蒙授音乐
I 其他艺术
J 蒙授其他艺术
K 汉授体育
L 蒙授体育
071 071西南大学
018 018西北政法大学
071 071西南大学
151 151周口师范学院
171 171西安建筑科技大学
269 269中国传媒大学
271 271浙江传媒学院
273 273中央戏剧学院
274 274上海戏剧学院
307 307北京师范大学
320 320陕西师范大学
325 325云南师范大学
421 421九江学院
598 598许昌学院
623 623四川音乐学院
630 630河北大学
752 752内蒙古师范大学
761 761内蒙古民族大学
767 767赤峰学院
803 803沈阳音乐学院
848 848吉林艺术学院
851 851吉林师范大学
852 852白城师范学院
876 876黑河学院
877 877东北农业大学
910 910南京艺术学院
927 927海南师范大学
941 941西北大学
A08 A08上海政法学院
B96 B96南阳理工学院
K00 K00山西传媒学院
K91 K91内蒙古艺术学院
L88 L88海南师范大学"""


def get_number(data):
    url = "https://www1.nm.zsks.cn/xxcx/gkcx/lqmaxmin_19.jsp"
    response = requests.post(url, data=data, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    try:
        table_list = soup.find_all('table')
        for one in table_list:
            data = one.select("td")
            for t in data:
                print(t.text)
    except Exception as e:
        print(1)
        pass


if __name__ == '__main__':
    data = {
        'm_yxdh': '{}',
        'query': '提交',
        'pcdm': '{}',
        'kldm': '{}',
        'pxfs': '1'
    }
    tem_data = tem_data.split("\n")
    pici = tem_data[0:10]
    kelei = tem_data[10:23]
    xuexiao = tem_data[24:]
    print(pici)
    print(kelei)
    print(xuexiao)
    for pi in pici:
        for ke in kelei:
            for x in xuexiao:
                data['m_yxdh'] = x.split(" ")[0]
                data['pcdm'] = pi.split(" ")[0]
                data['kldm'] = ke.split(" ")[0]
                get_number(data)
