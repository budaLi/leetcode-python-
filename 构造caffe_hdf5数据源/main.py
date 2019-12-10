# @Time    : 2019/12/10 18:14
# @Author  : Libuda
# @FileName: main.py
# @Software: PyCharm
# -*- coding: utf-8 -*-
'''
hdf5数据源
'''
import math
import numpy as np
import random
import re
import os
import h5py
import cv2

# 图片路径
root_path = '/home/pcb/caffe/examples/Caffe_DataMaker_hdh5/image'
with open('/home/pcb/caffe/examples/Caffe_DataMaker_hdh5/hdf5.txt', 'r') as f:
    lins = f.readlines()

num = len(lins)  # 数据长度

random.shuffle(lins)  # 把数据洗牌
imgAccu = 0
# 图片输入
# #制作Data,造一个224*224*3*图片个数的矩阵
imgs = np.zeros([num, 3, 224, 224])
# 制作label,造一个10(每个图像的标签数)×图片个数的矩阵
labels = np.zeros([num, 10])
for i in range(num):
    line = lins[i]
    # 使用正则表达式把串给分割开来，取第一个图片的名字  \s就是一个回车或者空格
    segment = re.split('\s+', line)
    # 找到图片
    image = cv2.imread(os.path.join(root_path, segment[0]))
    # 把图片进行缩小  把图片缩小到224  输入的大小就是224x224的
    image = cv2.resize(image, (224, 224))
    # 普通图片输入是h w c 而caffe要求是c h w，所以要转回来
    image = image.transpose(2, 0, 1)
    # 转类型,float32
    # 把数据都存在imge里面
    imgs[i, :, :, :] = image.astype(np.float32)
    # 因为图片缩小了，所以要吧label也要缩小
    for j in range(10):
        labels[i, j] = float(segment[j + 1]) * 224 / 256

# 每个hdf5文件里存放的个数,一般每个.h5里面放8000个
# 这里就3个，每个.h5里面放一个
batchSize = 1
# 取多少次
batchNum = int(math.ceil(1.0 * num / batchSize))

# 减去均值操作,目的是以0为中心化
# 在初始阶段减去均值后，最后预测的时候要加上
imgsMean = np.mean(imgs, axis=0)
labelsMean = np.mean(labels, axis=0)
labels = (labels - labelsMean) / 10

# 移除之前存在的文件
if os.path.exists('trainlist.txt'):
    os.remove('trainlist.txt')
if os.path.exists('testlist.txt'):
    os.remove('testlist.txt')

comp_kwargs = {'compression': 'gzip', 'compression_opts': 1}
for i in range(batchNum):
    start = i * batchSize
    end = min((i + 1) * batchSize, num)
    # 前面的几个bacthsize做为一个训练数据
    if i < batchNum - 1:
        fileName = '/home/pcb/caffe/examples/Caffe_DataMaker_hdh5/h5/train{0}.h5'.format(i)
    # 后面的一个作为测试集
    else:
        fileName = '/home/pcb/caffe/examples/Caffe_DataMaker_hdh5/h5/test{0}.h5'.format(i - batchNum + 1)

    # 往h5文件里面添加进数据
    with h5py.File(fileName, 'w') as f:
        f.create_dataset('data', data=np.array((imgs[start: end] - imgsMean) / 255.0).astype(np.float32), **comp_kwargs)
        f.create_dataset('label', data=np.array(labels[start: end]).astype(np.float32), **comp_kwargs)
        pass

    if i < batchNum - 1:
        with open('/home/pcb/caffe/examples/Caffe_DataMaker_hdh5/h5/trainlist.txt', 'a') as f:
            f.write(("/home/pcb/caffe/examples/Caffe_DataMaker_hdh5/h5/train{0}.h5").format(i) + '\n')
    else:
        with open('/home/pcb/caffe/examples/Caffe_DataMaker_hdh5/h5/testlist.txt', 'a') as f:
            f.write(("/home/pcb/caffe/examples/Caffe_DataMaker_hdh5/h5/test{0}.h5").format(i - batchNum + 1) + '\n')
