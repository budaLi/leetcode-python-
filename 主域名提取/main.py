# @Time    : 2020/2/21 15:54
# @Author  : Libuda
# @FileName: main.py
# @Software: PyCharm
import os

mainpath = os.getcwd()
filepath = os.getcwd() + "\\Email"
res = set()
for root, dirs, files in os.walk(filepath):
    for file in files:
        filepath = os.path.join(root, file)
        with open(filepath) as f:
            for data in f.readlines():
                data = data.split("/")
                try:
                    url = data[0] + "//" + data[2]
                except Exception as e:
                    url = data[0] + "//" + data[2]
                res.add(url)

    res_path = os.path.join(mainpath, "res.txt")
    with open(res_path, 'w') as f:
        for value in res:
            f.write(value + "\n")
    print("共提取主域名：{}个".format(len(res)))
    # print(files)
