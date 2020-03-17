# @Time    : 2020/3/15 18:55
# @Author  : Libuda
# @FileName: 公众号.py
# @Software: PyCharm
import re
import werobot

robot = werobot.WeRoBot(token='fandengdushu')


# 被关注自动回复
@robot.subscribe
def subscribe(message):
    return "樊登读书14天VIP免费领\n" + "回复手机号自动领取……\n" + "\n\n客服微信：95499954\n（找客服免费领取最新整理书单）"


# 接受信息自动回复
@robot.handler
def echo(message):
    message = message.content
    ret = re.match(r"^1[35678]\d{9}$", message)
    if ret:
        # 先看本地res中是否已经有开卡结果
        # res 中数据格式  手机号:13699679997,开卡结果:开卡失败,剩余链接数:10
        with open("res.txt") as f:
            res = f.readlines()
            for one in res:
                ph = one.rstrip().strip(",")[0].split(":")[1]
                if ph == message:
                    # 如果有此号码直接返回其开卡结果
                    return one
        # res中没有则写入phone 待开卡
        with open("phone.txt", 'a') as f:
            f.write(message + "\n")
        return "请耐心等候，正在查询您的开卡状态，为开卡将自动为您开卡"
    try:
        with open(message + ".txt", encoding="utf-8") as f:
            data = ".".join(f.readlines())
    except Exception:
        data = "此文件不在 请创建:{}".format("1")
    return data



if __name__ == '__main__':
    robot.config['HOST'] = '0.0.0.0'
    robot.config['PORT'] = 80

    robot.run()
