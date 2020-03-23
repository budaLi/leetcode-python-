# coding: utf-8
import re
import requests
import csv
import werobot

robot = werobot.WeRoBot(token='quant')
code_dict = {'PTA': 'TA0', 'pta': 'TA0', '菜油': 'OI0', 'OI': 'OI0', '菜籽': 'RS2009', 'RS': 'RS2009', '菜粕': 'RM0',
             'RM': 'RM0', '动力煤': 'ZC0', 'ZC': 'ZC0', '强麦': 'WH0', 'WH': 'WH0', '粳稻': 'JR0', 'JR': 'JR0', '白糖': 'SR0',
             'SR': 'SR0', '棉花': 'CF0', 'CF': 'CF0', '早籼稻': 'RI0', 'RI': 'RI0', '郑醇': 'MA0', 'MA': 'MA0', '玻璃': 'FG0',
             'FG': 'FG0', '晚籼稻': 'LR2003', 'LR': 'LR0', '硅铁': 'SF0', 'SF': 'SF0', '锰硅': 'SM0', 'SM': 'SM0', '棉纱': 'CY0',
             'CY': 'CY0', '苹果': 'AP0', 'AP': 'AP0', '红枣': 'CJ0', 'CJ': 'CJ0', '尿素': 'UR0', 'UR': 'UR0', '纯碱': 'SA0',
             'SA': 'SA0', 'PVC': 'V0', 'V': 'V0', '棕榈': 'P0', 'P': 'P0', '豆二': 'B0', 'B': 'B0', '豆粕': 'M0', 'M': 'M0',
             '铁矿石': 'I0', 'I': 'I0', '鸡蛋': 'JD0', 'JD': 'JD0', '塑料': 'L0', 'L': 'L0', 'PP': 'PP0', '纤维板': 'FB0',
             'FB': 'FB0', '胶合板': 'BB0', 'BB': 'BB0', '豆油': 'Y0', 'Y': 'Y0', '玉米': 'C0', 'C': 'C0', '豆一': 'A0',
             'A': 'A0', '焦炭': 'J0', 'J': 'J0', '焦煤': 'JM0', 'JM': 'JM0', '玉米淀粉': 'CS0', 'CS': 'CS0', '乙二醇': 'EG0',
             'EG': 'EG0', '粳米': 'RR0', 'RR': 'RR0', '苯乙烯': 'EB0', 'EB': 'EB0', '燃油': 'FU0', 'FU': 'FU0', '原油': 'SC0',
             'SC': 'SC0', '沪铝': 'AL0', 'AL': 'AL0', '橡胶': 'RU0', 'RU': 'RU0', '沪锌': 'ZN0', 'ZN': 'ZN0', '沪铜': 'CU0',
             'CU': 'CU0', '黄金': 'AU0', 'AU': 'AU0', '螺纹钢': 'RB0', '螺纹': 'RB0', 'RB': 'RB0', '线材': 'WR0', 'WR': 'WR0',
             '沪铅': 'PB0', '铅': 'PB0', 'PB': '铅', '白银': 'AG0', '银': 'AG0', 'AG': 'AG0', '沥青': 'BU0', 'BU': 'BU0',
             '热轧卷板': 'HC0', '热轧卷': 'HC0', 'HC': 'HC0', '沪锡': 'SN0', '锡': 'SN0', 'SN': 'SN0', '沪镍': 'NI0', '镍': 'NI0',
             'NI': 'NI0', '纸浆': 'SP0', 'SP': 'SP0', '20号胶': 'NR0', 'NR': 'NR0', '不锈钢': 'SS0', 'SS': 'SS0',
             '沪深300': 'IF0', 'IF': 'IF0', '5年期国债期货': 'TF0', 'TF': 'TF0', '10年期国债期货': 'T2006', 'T': 'T2006',
             '上证50': 'IH0', 'IH': 'IH0', '中证500': 'IC0', 'IC': 'IC0', '2年期国债期货': 'TS0', 'TS': 'TS0'}


# 被关注自动回复
# @robot.subscribe
def subscribe(message):
    return "hello~\n欢迎关注【期事】，如果您想获取实时期货价格，请直接输入品种名称\n比如：你想搜索螺纹，直接回复‘螺纹’或‘RB’\n获取期货交易模型或程序化软件请添加小编QQ/微信：876134889"


# 接受信息自动回复
# @robot.handler
def search(keyword):
    """查询股票或期货"""
    if keyword in code_dict.keys():
        var = code_dict.get(keyword)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'
        }

        url = "https://hq.sinajs.cn/list={}".format(var)
        resp = requests.get(url=url, headers=headers)
        data = ''.join(re.compile('"(.*?)"').findall(resp.text))
        data = data.split(',')
        return "您查询的品种是：{0}\n开盘价：{1}\n最高价：{2}\n最低价：{3}\n昨天收盘价：{4}\n实时买价：{5}\n实时卖价：{6}\n实时最新价：{7}".format(keyword,
                                                                                                         data[2],
                                                                                                         data[3],
                                                                                                         data[4],
                                                                                                         data[5],
                                                                                                         data[6],
                                                                                                         data[7],
                                                                                                         data[8])
    else:
        return "hello~\n欢迎关注【期事】，如果您想获取实时期货价格，请直接输入品种名称\n比如：你想搜索螺纹，直接回复‘螺纹’或‘RB’\n获取期货交易模型或程序化软件请添加小编QQ/微信：876134889"
    # return "hello~\n欢迎关注【期事】，如果您想获取实时期货价格，请直接输入品种名称\n比如：你想搜索螺纹，直接回复‘螺纹’或‘RB’\n获取期货交易模型或程序化软件请添加小编QQ/微信：876134889"


# robot.config['HOST'] = '0.0.0.0'
# robot.config['PORT'] = 80
#
# robot.run()

print(search('螺纹'))
