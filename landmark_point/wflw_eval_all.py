# coding:utf-8
from __future__ import print_function
import os
import numpy as np
import sys
import json
import cv2
import csv
import time

sys.path.append('../../caffe/python')
import caffe

sys.path.append('../../tools/landmark_eval_tools')
from wflw_eval_tool import landmark_eval_IPN


def landmark_txt_to_array(file_path, num_of_landmark):
    """
    将label数据拆分成图片路径,人脸框位置，关键点
    :param file_path: 文件位置
    :param num_of_landmark:关键点数量
    :return:
    """
    all_landmarks = []
    all_boxs = []
    all_images = []
    fr = open(file_path, 'r')
    line = fr.readline().rstrip()
    while line:
        all_images.append(line)
        line = fr.readline().rstrip()
        ord = line.split(' ')
        all_boxs.append([float(tk) for tk in ord])
        landmarks = []
        for i in range(num_of_landmark):
            line = fr.readline().rstrip()
            ord = line.split(' ')
            landmarks.append([float(tk) for tk in ord])
        all_landmarks.append(landmarks)
        line = fr.readline().rstrip()
    return all_images, all_boxs, all_landmarks


def draw_landmark(src_img_dir, out_path, gt_landmark_path, detect_landmark_path, num_of_landmark):
    print("draw_landmark")
    if not os.path.isdir(out_path):
        os.makedirs(out_path)
    gt_all_images, gt_all_boxs, gt_all_landmarks = landmark_txt_to_array(gt_landmark_path, 98)
    all_images, all_boxs, all_landmarks = landmark_txt_to_array(detect_landmark_path, num_of_landmark)
    for i in range(len(all_images)):
        img_path = os.path.join(src_img_dir, all_images[i])
        img = cv2.imread(img_path)
        box = np.array(all_boxs[i], dtype=np.int)
        gt_box = np.array(gt_all_boxs[i], dtype=np.int)
        color = (0, 0, 255)

        cv2.rectangle(img, (gt_box[0], gt_box[1]), (gt_box[2] + gt_box[0], gt_box[3] + gt_box[1]), color, 2)

        # 真实的关键点  绿色
        gt_landmark = np.array(gt_all_landmarks[i], dtype=np.int)
        for j in range(num_of_landmark):
            color = (0, 255, 0)
            cv2.circle(img, (gt_landmark[j][0], gt_landmark[j][1]), 1, color, 3)

        # 检测出来的关键点  蓝色
        landmark = np.array(all_landmarks[i], dtype=np.int)
        for j in range(num_of_landmark):
            color = (255, 0, 0)
            cv2.circle(img, (landmark[j][0], landmark[j][1]), 1, color, 3)
        detect_img = str(i) + '_' + os.path.basename(all_images[i])
        detect_img_path = os.path.join(out_path, detect_img)
        cv2.imwrite(detect_img_path, img)


def landmark_forward(l_net, im, det):
    """
    通过检测网络获取landmark 及 耗费的时间
    :param l_net:
    :param im:
    :param det:
    :return:
    """
    # start_time = time.time()
    caffe_img = im.copy()
    x, y, w, h = int(det[0]), int(det[1]), int(det[2]), int(det[3])

    # 训练数据集 人脸框扩大 测试时也必须扩大
    box_size = int(max(w, h) * 1.2)

    x1 = int(x + 0.5 * w - box_size * 0.5)
    y1 = int(y + 0.5 * h - box_size * 0.5)
    x2 = x1 + box_size
    y2 = y1 + box_size
    dx = max(0, -x1)
    dy = max(0, -y1)
    x1 = max(0, x1)
    y1 = max(0, y1)
    edx = max(0, x2 - caffe_img.shape[1])
    edy = max(0, y2 - caffe_img.shape[0])
    x2 = min(caffe_img.shape[1], x2)
    y2 = min(caffe_img.shape[0], y2)

    crop_img = caffe_img[int(y1):int(y2), int(x1):int(x2)]
    if (dx > 0 or dy > 0 or edx > 0 or edy > 0):
        # print(dx, dx, edx, edy)
        crop_img = cv2.copyMakeBorder(crop_img, dy, edy, dx, edx, cv2.BORDER_CONSTANT, 0)

    # 减均值
    crop_img = (crop_img - 127.5) / 128
    h_img, w_img, c = crop_img.shape

    scale_img = cv2.resize(crop_img, (48, 48), interpolation=cv2.INTER_LINEAR)

    # 两个函数的差异
    x = scale_img.transpose(2, 0, 1)
    # x = np.swapaxes(scale_img, 0, 2)

    l_net.blobs['data'].data[...][0] = x
    start_time = time.time()
    l_net.forward()
    # end_time = time.time()
    l_out_land = l_net.blobs['output'].data[0].flatten()

    l_out_pix_land = l_out_land
    l_out_pix_land[0::2] = l_out_land[0::2] * w_img + x1
    l_out_pix_land[1::2] = l_out_land[1::2] * h_img + y1

    landmarks = []
    for i in range(len(l_out_pix_land)):
        point = []
        if (i % 2 == 0):
            point.append(l_out_pix_land[i])
            point.append(l_out_pix_land[i + 1])
            landmarks.append(point)
    end_time = time.time()
    return landmarks, (end_time - start_time)


def main(iter_num):
    """
    评测不同模型的结果
    :param iter_num:模型迭代次数
    :return:返回该模型测试各个子数据集的nme, failure_rate, auc
    例子：{
            "list_98pt_test_blur.txt":
                                {
                                    "nme":"",
                                    "failure_rate:"",
                                    "auc":"",
                                }

            "list_98pt_test_expression.txt":
                                {
                                    ...
                                }
        }
    """

    # 存放返回结果
    res = []

    # 网络配置
    o_prototxt = '/raid1/ljj/face_landmark/src/prototxt/nmv2.prototxt'

    # # 测试模型迭代次数
    # iter_num = 220000

    # 工程根目录
    base_dir_path = "/raid1/ljj/face_landmark"

    # 模型存放路径

    model = os.path.join(base_dir_path, 'models/nmv-4-2-98-point/nmv-98-point_iter_{}.caffemodel'.format(iter_num))

    # 输出的文件夹名
    l_name = 'mvw_ca_{}'.format(iter_num)

    # 输出csv文件的路径
    txt_name = os.path.join(base_dir_path, "output/wflw_test/mvw_ca-98_to_5.csv")

    # 输出文件路径
    out_path = '/raid1/ljj/face_landmark/output/wflw_test/' + l_name + '/' + str(iter_num) + "/"

    # WFLW 图片存放路径
    dataset_path = '/raid1/ljj/dataset/WFLW/WFLW_images'

    # ground truth 文件名  对应WFLW 数据集不同子集
    ground_truth_txt = ["list_98pt_test_blur.txt", "list_98pt_test_expression.txt",
                        "list_98pt_test_illumination.txt", "list_98pt_test_largepose.txt",
                        "list_98pt_test_makeup.txt", "list_98pt_test_occlusion.txt"]

    base_ground_truth_path = "/raid1/ljj/face_landmark/tools/wflw_split/label_datas/out/"

    # 存放WFLW子集的真实路径
    ground_truth_txt_path = [os.path.join(base_ground_truth_path, one) for one in ground_truth_txt]

    # 输出文件名 不同子集对应不同的输出文件名
    detect_landmark_txt = ['wflw_detect_landmark-{}-{}'.format(iter_num, one) for one in ground_truth_txt]

    # 输出文件的真实路径
    detect_txt = [os.path.join(out_path, one) for one in detect_landmark_txt]

    # 输出auc ced图片的路径及名称
    pic_out_path = [os.path.join(out_path, one) for one in ground_truth_txt]

    # 配置caffe
    caffe.set_mode_gpu()
    caffe.set_device(0)

    # 是否绘制landmark
    draw_flag = True
    total_time = 0

    print('Loading the network...', end="")
    # 初始 caffe 测试网络
    l_net = caffe.Net(o_prototxt, model, caffe.TEST)
    # 测试网络名称
    l_net.name = 'Landmark'
    print('Loading the network done!')

    if not os.path.isdir(out_path):
        # 没有输出文件则递归创建  权限问题可 chmod 777 更改文件权限
        os.makedirs(out_path)

    # 遍历每个子数据集
    for gd_ttuth_index in range(len(ground_truth_txt_path)):

        # 存储图片
        img_list = []

        # 存储人脸框
        bbx_list = []

        with open(ground_truth_txt_path[gd_ttuth_index]) as fr:
            totle_datas = fr.readlines()

            # 只需要提取 图片路径和 人脸框
            for index in range(0, len(totle_datas), 100):
                img_list.append(totle_datas[index])
                # 人脸框为图片路径的下一行
                bbx = totle_datas[index + 1].rstrip()
                # 人脸框信息转换为float存储
                bbx_tem = bbx.split(" ")
                bbx_list.append([float(x) for x in bbx_tem])

        with open(detect_txt[gd_ttuth_index], 'w') as fw:
            # 对于检测的每一个图片进行检测 将其结果写入
            for img_index in range(len(img_list)):
                # 拼接图片路径
                im_path = os.path.join(dataset_path, img_list[img_index])
                face = bbx_list[img_index]
                # 这里要注意图片路径不能有换行符
                img = cv2.imread(im_path.rstrip())
                landmark, timer = landmark_forward(l_net, img, face)
                total_time += timer
                # 图片读入时已经有换行 需去除 否则写入文件时有空行
                fw.write(img_list[img_index].strip() + '\n')
                fw.write('%d %d %d %d\n' % (int(face[0]), int(face[1]), int(face[2]), int(face[3])))
                # fw.write('%d %d %d %d\n'.format(int(face[0]), int(face[1]), int(face[2]), int(face[3])))
                for j in range(len(landmark)):
                    point = landmark[j]
                    fw.write('%.4f %.4f\n' % (point[0], point[1]))

        # 计算 nme, failure_rate, auc
        #  要注意 检测的是98 点还是  5点的 参数不同
        # 98，5  检测到98点测试5点
        nme, failure_rate, auc = landmark_eval_IPN(pic_out_path[gd_ttuth_index], ground_truth_txt_path[gd_ttuth_index],
                                                   detect_txt[gd_ttuth_index], 98, 5, l_name)

        # 拼接返回结果
        res.append([nme, failure_rate, auc * 10])

        if draw_flag:
            copy_path = os.path.join(out_path, '{}_new_images'.format(iter_num))
            copy_path = os.path.join(copy_path, ground_truth_txt[gd_ttuth_index])
            draw_landmark(dataset_path, copy_path, ground_truth_txt_path[gd_ttuth_index], detect_txt[gd_ttuth_index],
                          98)

    # a+表示追加到csv文件中
    with open(txt_name, 'a+') as f:
        writer = csv.writer(f)
        # 需要写入多少列就循环多少次
        row_item = [iter_num]
        # 每个子集
        for i in range(len(res)):
            # nme,failure_rate,auc
            for one in res[i]:
                row_item.append(one)
            # 优化显示
            row_item.append(" ")
        writer.writerow(row_item)

    # indent 设置换行 方便查看
    # json_data = json.dumps(res,indent=4)
    # json_data = json.dumps(res)

    # 追加写入json文件
    # with open("data.json","a+") as f:
    #     f.write(json_data+"\n")

    print("ok")


if __name__ == "__main__":

    # 模型的迭代次数 可同时评测多个模型
    lis = [510000]
    for i in lis:
        res1 = main(i)
