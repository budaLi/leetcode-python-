# @Time    : 2020/4/26 16:24
# @Author  : Libuda
# @FileName: test.py
# @Software: PyCharm
import numpy as np
from copy import deepcopy
import sys

# 问题： 通过draw_ground_truth_landmark.py 发现WFLW数据集标注的人脸框不是很准确
#  存在关键点在人脸框之外的情况 而caffe模型推理生成的关键点坐标是相对于人脸框的绝对位置
# 那么该如何去评测  现在采取的方法是评测时将关键点加上人脸框位置变为相对于图片的绝对坐标

sys.path.append("./")
from utils import compute_5points5_ION_NME, compute_98points5_ION_NME, compute_98points98_ION_NME, compute_AUC, \
    compute_FAR

# ssh人脸框
box_txt = "wflw_detect_test.txt"
# 真实关键点文件
ground_truth_txt = 'list_98pt_rect_attr_test.txt'
# 检测结果
detect_txt = "checkpoint_epoch_120_caffe_list.txt"


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

        landmark = np.asarray(landmark, dtype=np.float32).reshape(98, 2)
        attribute = np.asarray(attribute, dtype=np.int32)
        box = np.asarray(box, dtype=np.int32)

        # landmark = landmark - (box[0], box[1])

        filenames.append(path)
        landmarks.append(landmark)
        attributes.append(attribute)
        boxs.append(box)

    filenames = np.asarray(filenames, dtype=np.str)
    landmarks = np.asarray(landmarks, dtype=np.float32)
    attributes = np.asarray(attributes, dtype=np.int32)
    boxs = np.asarray(boxs, dtype=np.int32)

    return (filenames, landmarks, attributes, boxs)


def load_detect_data_by_ssh_detect(detect_txt, point=98):
    """
    加载ssh检测数据
    :return:
    """

    # 人脸框 检测出来的关键点要根据人脸框进行坐标转换
    boxsizes = []
    tem = []
    with open(box_txt) as f:
        lines = f.readlines()
        for i in range(1, len(lines), 2):
            x, y, w, h = list(map(int, lines[i].strip().split()))
            d_boxsize = max(w, h)
            boxsizes.append(d_boxsize)
            d_center_x, d_center_y = x + w // 2, y + h // 2

            d_new_x1 = d_center_x - d_boxsize // 2
            d_new_y1 = d_center_y - d_boxsize // 2
            tem.append([d_new_x1, d_new_y1])

    # 提取检测数据中的图片名和关键点
    with open(detect_txt) as f:
        detect_lines = f.readlines()
        detect_filename, detect_landmarks = [], []
        for index in range(0, len(detect_lines), point + 1):
            tem_landmark = []
            detect_filename.append(detect_lines[index].strip())
            landmark = detect_lines[index + 1:index + point + 1]
            for ldmk in landmark:
                x, y = ldmk.strip().split()
                i = int(index / (point + 1))
                x = round(float(x) * boxsizes[i] + tem[i][0], 6)
                y = round(float(y) * boxsizes[i] + tem[i][1], 6)
                tem_landmark.append(np.asarray([x, y], dtype=np.float32))
            detect_landmarks.append(tem_landmark)
    detect_landmarks = np.asarray(detect_landmarks, dtype=np.float32)
    return detect_filename, detect_landmarks


def load_detect_data_by_wflw_box(detect_txt, point=98):
    """
    要和制作测试集一样使用wflw关键点作为人脸框 进行坐标转换
    :param detect_txt:
    :param point:
    :return:
    """
    boxsizes = []
    tem = []
    with open(ground_truth_txt) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip().split()
            landmark = np.asarray(list(map(float, line[:196])), dtype=np.float32).reshape(-1, 2)
            xy = np.min(landmark, axis=0).astype(np.int32)
            zz = np.max(landmark, axis=0).astype(np.int32)
            wh = zz - xy + 1

            center = (xy + wh / 2).astype(np.int32)
            boxsize = int(np.max(wh) * 1.2)
            xy = center - boxsize // 2
            x1, y1 = xy
            boxsizes.append(boxsize)
            tem.append([x1, y1])

    # 提取检测数据中的图片名和关键点
    with open(detect_txt) as f:
        detect_lines = f.readlines()
        detect_filename, detect_landmarks = [], []
        for index in range(0, len(detect_lines), point + 1):
            tem_landmark = []
            detect_filename.append(detect_lines[index].strip())
            landmark = detect_lines[index + 1:index + point + 1]
            for ldmk in landmark:
                x, y = ldmk.strip().split()
                i = int(index / (point + 1))
                x = round(float(x) * boxsizes[i] + tem[i][0], 6)
                y = round(float(y) * boxsizes[i] + tem[i][1], 6)
                tem_landmark.append(np.asarray([x, y], dtype=np.float32))
            detect_landmarks.append(tem_landmark)
    detect_landmarks = np.asarray(detect_landmarks, dtype=np.float32)
    return detect_filename, detect_landmarks


def main():
    # 总的测试数据
    filenames, landmarks, attributes, boxs = load_ground_data(ground_truth_txt)

    # 检测数据
    detect_filename, detect_landmarks = load_detect_data_by_wflw_box(detect_txt, point=98)


    #  6 种不同子集的索引  [false,false,true....]
    # 200: 姿态(pose)         0->正常姿态(normal pose)          1->大的姿态(large pose)
    # 201: 表情(expression)   0->正常表情(normal expression)    1->夸张的表情(exaggerate expression)
    # 202: 照度(illumination) 0->正常照明(normal illumination)  1->极端照明(extreme illumination)
    # 203: 化妆(make-up)      0->无化妆(no make-up)             1->化妆(make-up)
    # 204: 遮挡(occlusion)    0->无遮挡(no occlusion)           1->遮挡(occlusion)
    # 205: 模糊(blur)         0->清晰(clear)                    1->模糊(blur)

    totle_data = []
    # totle_data = [[range(0,10)]]
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

        error_per_image, error_per_point, nme = compute_98points98_ION_NME(ground_truth_all=tem_ground_truth_landmark,
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
