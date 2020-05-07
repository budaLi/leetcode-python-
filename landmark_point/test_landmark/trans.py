# @Time    : 2020/4/26 16:24
# @Author  : Libuda
# @FileName: test.py
# @Software: PyCharm
import numpy as np
from copy import deepcopy
import sys

sys.path.append("./")
from utils import compute_5points5_ION_NME, compute_98points5_ION_NME, compute_AUC, compute_FAR

# 真实关键点文件
ground_truth_txt = 'list_98pt_rect_attr_test.txt'
# 检测结果
detect_txt = "caffe_list.txt"


def load_ground_data(file_list):
    """
    加载测试数据
    :param file_list:
    :return:
    """
    with open(file_list, 'r') as f:
        lines = f.readlines()
    filenames, landmarks, attributes, boxs = [], [], [], []
    for line in lines:
        line = line.strip().split()
        path = line[-1]
        landmark = line[0:196]
        box = line[196:200]
        attribute = line[200:206]

        landmark = np.asarray(landmark, dtype=np.float32).reshape((-1, 98, 2))
        attribute = np.asarray(attribute, dtype=np.int32)
        box = np.asarray(box, dtype=np.int32)

        landmark = landmark - (box[0], box[1])

        filenames.append(path)
        landmarks.append(landmark)
        attributes.append(attribute)
        boxs.append(box)

    filenames = np.asarray(filenames, dtype=np.str)
    landmarks = np.asarray(landmarks, dtype=np.float32)
    attributes = np.asarray(attributes, dtype=np.int32)
    boxs = np.asarray(boxs, dtype=np.int32)

    return (filenames, landmarks, attributes, boxs)


def load_detect_data(detect_txt, point=5):
    """
    加载检测数据
    :return:
    """
    # 提取检测数据中的图片名和关键点
    with open(detect_txt) as f:
        detect_lines = f.readlines()
        detect_filename, detect_landmarks = [], []
        for index in range(0, len(detect_lines), point + 1):
            tem_landmark = []
            detect_filename.append(detect_lines[index].strip())
            landmark = detect_lines[index + 1:index + point + 1]
            for ldmk in landmark:
                tem_landmark.append(np.asarray(ldmk.split(), dtype=np.float32))
            detect_landmarks.append(tem_landmark)
    detect_landmarks = np.asarray(detect_landmarks, dtype=np.float32)
    return detect_filename, detect_landmarks


def main():
    # 总的测试数据
    filenames, landmarks, attributes, boxs = load_ground_data(ground_truth_txt)

    # 检测数据
    detect_filename, detect_landmarks = load_detect_data(detect_txt, point=98)

    totle_data = []

    #  6 种不同子集的索引  [false,false,true....]
    # 200: 姿态(pose)         0->正常姿态(normal pose)          1->大的姿态(large pose)
    # 201: 表情(expression)   0->正常表情(normal expression)    1->夸张的表情(exaggerate expression)
    # 202: 照度(illumination) 0->正常照明(normal illumination)  1->极端照明(extreme illumination)
    # 203: 化妆(make-up)      0->无化妆(no make-up)             1->化妆(make-up)
    # 204: 遮挡(occlusion)    0->无遮挡(no occlusion)           1->遮挡(occlusion)
    # 205: 模糊(blur)         0->清晰(clear)                    1->模糊(blur)
    for i in range(6):
        totle_data.append(np.where(attributes[:, i] == 1))

    nme_lis = []
    acu_lis = []
    failure_rate_lis = []

    for data in totle_data:
        # 测试用的gd landmark
        tem_ground_truth_landmark = []
        tem_detect_landmark = []

        for index in data[0]:
            tem_ground_truth_landmark.append(landmarks[index])
            tem_detect_landmark.append(detect_landmarks[index])

        error_per_image, error_per_point, nme = compute_98points5_ION_NME(ground_truth_all=tem_ground_truth_landmark,
                                                                          detect_landmark_all=tem_detect_landmark)
        _, _, auc = compute_AUC(error_per_point, x_limit=0.1)
        failure_rate = compute_FAR(error_per_image, thresh=0.1)

        nme_lis.append(nme)
        acu_lis.append(auc)
        failure_rate_lis.append(failure_rate)

    # 整体平均值
    totle_mean_nme = np.mean(nme_lis)
    totle_mean_auc = np.mean(acu_lis)
    totle_mean_fr = np.mean(failure_rate_lis)
    return (totle_mean_nme, totle_mean_auc, totle_mean_fr), (nme_lis, acu_lis, failure_rate_lis)


if __name__ == '__main__':
    totle_res, (nme_lis, auc_lis, failure_rate_lis) = main()
    print(totle_res)
    print("nme:{}".format(nme_lis))
    print("auc:{}".format(auc_lis))
    print("failure_rate:{}".format(failure_rate_lis))
