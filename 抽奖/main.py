# @Time    : 2020/2/23 23:04
# @Author  : Libuda
# @FileName: main.py
# @Software: PyCharm
import random

dict = {0: "谢谢惠顾", 1: "1天体验卡", 2: "3天体验卡", 3: "7天体验卡", 4: "7天体验卡", 5: "一生一世", 6: "三生三世", 7: "7天体验卡"}
print("欢迎使用嘟嘟专用抽奖系统！")
print("*" * 20)
chose = input("请输入您的抽奖次数：")
try:
    chose = int(chose)
except Exception:
    print("请输出数字 别瞎摁")
if isinstance(chose, int):
    index = 0
    for ix in range(chose):
        print("第{}次抽奖结果:{}".format(ix, dict[random.randint(0, 4)]))
exit = input("输入任意键退出本次抽奖")
