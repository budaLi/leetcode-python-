# @Time    : 2020/1/16 18:13
# @Author  : Libuda
# @FileName: 最小字典序.py
# @Software: PyCharm

def Solution(data):
    """
    输入：
    "AABACBBC"
    输出：
    "AAABBBCC"
    :param m:
    :return:
    """
    index = 0
    lenght = len(data) - 1
    data = list(data)

    while index < lenght:
        if data[index] > data[index + 1]:
            print("".join(data))
            if ord(data[index]) - ord(data[index + 1]) == 1:
                "ABABAB—> AABBAB "
                "当位置1和位置2交换后 需要从2开始找最近一个比他小的A交换"
                data[index], data[index + 1] = data[index + 1], data[index]
                tem = index + 1  # 记录当前进行到哪一个字符 "B"
                while tem < lenght:
                    if data[tem] == "A":
                        data[index + 1] = "A"
                        data[tem] = "B"
                        break
                    tem += 1
                index += 1
            else:
                "CAAAAB 这种情况 需要找到最近的一个B进行交换 变成BCAAAA这种"
                tem = index  # 记录当前进行到哪一个字符 "C"
                while index < lenght:
                    index += 1
                    if data[index] == "B":
                        data[tem + 1] = data[tem]
                        data[tem] = data[index]
                        data[tem + 2:index + 1] = "A" * (index - tem - 2 + 1)
        index += 1

    return "".join(data)


tem = "AABABAABBC"
res = Solution(tem)
# print(res)
