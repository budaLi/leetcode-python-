# @Time    : 2020/4/23 16:14
# @Author  : Libuda
# @FileName: demo-1.py
# @Software: PyCharm
# pip install --upgrade --ignore-installed tensorflow
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow import keras

fashion_mnist = keras.datasets.fashion_mnist
# 共六万图片
(x_train_all, y_train_all), (x_test, y_test) = fashion_mnist.load_data()
x_valid, x_train = x_train_all[:5000], x_train_all[5000:]
y_valid, y_train = y_train_all[:5000], y_train_all[5000:]

print(x_valid.shape, y_valid.shape)
print(x_train.shape, y_train.shape)
print(x_test.shape, y_test.shape)


def show_single_image(img_arr):
    plt.imshow(img_arr, cmap="binary")
    plt.show()


class_names = ["T-shirt", "Trouser", "Pullover", "Dress", "Coat"
    , "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"]


def show_images(n_rows, n_cols, x_data, y_data, class_names):
    assert len(x_data) == len(y_data)
    assert n_rows * n_cols < len(x_data)
    plt.figure(figsize=(n_cols * 1.4, n_rows * 1.6))
    for row in range(n_rows):
        for col in range(n_cols):
            index = n_cols * n_rows + col
            plt.subplot(n_rows, n_cols, index + 1)
            plt.imshow(x_data[index], cmap="binary", interpolation="nearest")
            plt.axis("off")
            plt.title(class_names[y_data[index]])

    plt.show()


if __name__ == '__main__':
    show_single_image(x_train[0])
    # show_images(1,1,x_train,y_train,class_names)
