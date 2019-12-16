# @Time    : 2019/12/13 11:20
# @Author  : Libuda
# @FileName: create_txt.py
# @Software: PyCharm

# @Time    : 2019/12/13 11:12
# @Author  : Libuda
# @FileName: create_txt.py
# @Software: PyCharm
import os

train_file_path = r"C:\Users\lenovo\PycharmProjects\insightface\data\re\train"
train_res_txt_path = r"C:\Users\lenovo\PycharmProjects\insightface\mylearn\train.txt"

test_file_path = r"C:\Users\lenovo\PycharmProjects\insightface\data\re\test"
test_res_txt_path = r"C:\Users\lenovo\PycharmProjects\insightface\mylearn\test.txt"

with open(train_res_txt_path, 'w') as f:
    print(123)
    for root, dir, files in os.walk(train_file_path):
        root = root.split("\\")[-1]
        for file in files:
            label = str(int(int(file.split(".")[0]) / 100) - 3)
            tem = root + "/" + file
            print(tem)
            f.write(tem + " " + label + "\n")
