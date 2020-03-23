# @Time    : 2020/1/19 14:54
# @Author  : Libuda
# @FileName: 洗牌算法.py
# @Software: PyCharm
import random
import math


class Shuffle():
    def Solution(self, data):
        """
        算法原理 所谓公平的洗牌算法 就是使得一个待打乱数组中 每一个数字在每一个位置出现的概率相同
        以[1.2.3.4.5] 举例  洗牌算法从 最后一个数字开始  将其位置n与前n个数据中随机的一个数据交换 第二次使第
        n-1的数字 与前n-1个数字中的一个随机数字交换
        :return:
        """
        for i in range(len(data) - 1, -1, -1):
            rd = random.randint(0, i)
            data[i], data[rd] = data[rd], data[i]

        return data


if __name__ == '__main__':
    S = Shuffle()
    data = [1, 2, 3, 4]
    res = S.Solution(data)

    print(res)
