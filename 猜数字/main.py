# @Time    : 2020/5/14 11:02
# @Author  : Libuda
# @FileName: main.py
# @Software: PyCharm

import pandas as pd
import random
import matplotlib.pyplot as plt
import matplotlib


def guessnum(Number):
    """
    传入数字返回猜到这个数字用的次数
    :param Number:
    :return:
    """
    n = 0
    Min = 0
    Max = 10
    # Number = random.randint(0, 100)  # 随机生成0-100的整数
    flag = True
    Num = random.randint(0, 10)

    while flag:
        if Num < Number:
            Min = Num
            b = Max - Min
            c = b // 2
            Num += c
            n += 1
        elif Num > Number:
            Max = Num
            b = Max - Min
            c = b // 2
            Num -= c
            n += 1
        else:
            flag = False

    return Number, n


def res_to_csv(Number, guss_count):
    """
    将数字及其猜测次数保存到csv
    :param Number:
    :param guss_count:
    :return:
    """
    excel_path = "res.xls"
    old_data = pd.read_excel(excel_path)
    df = pd.DataFrame(old_data)
    result = []
    res = {}
    res["Number"] = str(Number)
    res["guss_count"] = str(guss_count)
    result.append(res)

    # 最恶心的地方就是必须将其返回
    df = df.append(result)
    df.to_excel(excel_path, sheet_name='biubiu', index=0)


def show_res():
    # 设置matplotlib正常显示中文和负号
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    matplotlib.rcParams['axes.unicode_minus'] = False
    data = pd.read_excel("res.xls")
    Number = data["Number"]
    guss_count = data['guss_count']
    # num_list2 = [15, 30, 40, 20]  # 纵坐标值2
    # x = range(len(num_list1))
    """
    绘制条形图
    left:长条形中点横坐标
    height:长条形高度
    width:长条形宽度，默认值0.8
    label:为后面设置legend准备
    """
    plt.bar(left=Number, height=guss_count, width=0.4, alpha=0.8, color='red')
    plt.ylim(0, 10)  # y轴取值范围
    plt.ylabel("猜测次数")
    plt.xticks([index + 0.2 for index in Number], Number)
    # plt.xticks([index  for index in x], label_list)
    plt.xlabel("预想值")
    plt.title("AI猜数可视化")
    plt.legend()  # 设置题注
    # 编辑文本

    for a, b in zip(Number, guss_count):
        print(a, b)
        plt.text(a, b + 0.1, '%.0f' % b, ha='center', va='bottom', fontsize=7)

    # for rect in rects1:
    #     height = rect.get_height()
    #     plt.text(rect.get_x() + rect.get_width() / 2, height + 1,height, ha="center", va="bottom")
    plt.show()


def main():
    # 0-10为预先想好的数字
    for i in range(1, 10):
        print(i)
        number, guss_count = guessnum(i)
        print("数字%s,猜了%s次" % (number, guss_count))
        res_to_csv(number, guss_count)
        # print("——————————")


if __name__ == '__main__':
    # 注意 猜测同样的数字需将excel情况 否则可视化显示有问题

    # 1.猜测数字并写入excel
    # main()

    # 2.可视化
    show_res()
