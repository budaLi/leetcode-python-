# coding: utf-8
import re
import requests
import werobot

robot = werobot.WeRoBot(token='quant')


def load_csv(file_path):
    """读取CSV文件为字典格式"""
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        res = dict(line.strip().split(',') for line in f if line)
        return res


code_dict = load_csv("qh_code.csv")
zjs_dict = load_csv("zjs_code.csv")


def load_txt(file_path):
    """读取txt文档设为自动回复内容"""
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        res = f.read()
        return res


txt = load_txt("guanzhu.txt")
yw_txt = load_txt("yw_txt.txt")
shouxufei_txt = load_txt("shouxufei.txt")


# 被关注自动回复
@robot.subscribe
def subscribe(message):
    return txt


# 接受信息自动回复
@robot.handler
def echo(keyword):
    """查询股票或期货"""
    if keyword.content in code_dict:
        var = code_dict.get(keyword.content)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'
        }

        url = r"https://hq.sinajs.cn/list=nf_{0}".format(var)
        resp = requests.get(url=url, headers=headers)
        print("res", resp.text, "keyword", var)
        data = ''.join(re.compile('"(.*?)"').findall(resp.text))
        data = data.split(',')
        print(data)
        return "您查询的品种是：{0}\n开盘价：{1}\n最高价：{2}\n最低价：{3}\n昨天收盘价：{4}\n实时买价：{5}\n实时卖价：{6}\n实时最新价：{7}\n\n{8}".format(
            keyword.content, data[2], data[3], data[4], data[5], data[6], data[7], data[8], yw_txt)

    elif keyword.content in zjs_dict:
        var = zjs_dict.get(keyword.content)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'
        }
        url = r"https://hq.sinajs.cn/list=nf_{0}".format(var)
        resp = requests.get(url=url, headers=headers)
        data = ''.join(re.compile('"(.*?)"').findall(resp.text))
        data = data.split(',')
        return "您查询的品种是：{0}\n开盘价：{1}\n最高价：{2}\n最低价：{3}\n昨天收盘价：{4}\n\n{5}".format(keyword.content, data[0], data[1],
                                                                                 data[2], data[3], yw_txt)
    elif "手续费" in keyword.content:
        return shouxufei_txt
    else:
        return txt
    # return "hello~\n欢迎关注【期事】，如果您想获取实时期货价格，请直接输入品种名称\n比如：你想搜索螺纹，直接回复‘螺纹’或‘RB’\n获取期货交易模型或程序化软件请添加小编QQ/微信：876134889"


robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80

robot.run()
