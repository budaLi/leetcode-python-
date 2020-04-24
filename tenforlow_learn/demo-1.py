# @Time    : 2020/4/23 16:14
# @Author  : Libuda
# @FileName: demo-1.py
# @Software: PyCharm
# pip install --upgrade --ignore-installed tensorflow
import matplotlib as mpl
import os
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import pandas as pd
from tensorflow import keras
from sklearn.preprocessing import StandardScaler

fashion_mnist = keras.datasets.fashion_mnist
# 共六万图片
(x_train_all, y_train_all), (x_test, y_test) = fashion_mnist.load_data()
x_valid, x_train = x_train_all[:5000], x_train_all[5000:]
y_valid, y_train = y_train_all[:5000], y_train_all[5000:]

print(np.max(x_train), np.min(x_train))

# 做归一化
scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train.astype(np.float32).reshape(-1, 1)).reshape(-1, 28, 28)

x_valid_scaled = scaler.transform(x_valid.astype(np.float32).reshape(-1, 1)).reshape(-1, 28, 28)

x_test_scaled = scaler.transform(x_test.astype(np.float32).reshape(-1, 1)).reshape(-1, 28, 28)

print(np.max(x_train_scaled), np.min(x_train_scaled))

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
            # index 表示在n_rows行 n_cols列中的 哪个地方画图 取值范围为1，n_rows*n_cols
            index = n_rows * n_cols - col - row * n_cols
            plt.subplot(n_rows, n_cols, index)
            plt.imshow(x_data[index], cmap="binary", interpolation="nearest")
            plt.axis("off")
            plt.title(class_names[y_data[index]])

    plt.show()


def train():
    models = keras.models.Sequential()
    # 输入28*28的图像数据 28*28的矩阵变为 1*726的一维向量
    models.add(keras.layers.Flatten(input_shape=[28, 28]))
    # 全连接层 relu激活函数
    models.add(keras.layers.Dense(300, activation="relu"))

    models.add(keras.layers.Dense(100, activation="relu"))

    # softmax将向量变成概率分布
    # x= [x1,x2,x3]
    # y = [e^x1/sum,e^x2/sum,e^x3/sum],sum = e^x1+e^x2+e^x3
    models.add(keras.layers.Dense(10, activation="softmax"))

    models.compile(loss="sparse_categorical_crossentropy",
                   optimizer="sgd",
                   metrics=["accuracy"])

    # 模型的层
    print(models.layers)

    # 可以看到模型的参数
    print(models.summary())

    # TensorBoard  earlytopping ModelCheckpoint

    log_dir = "callbacks"
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    ouput_model_file = os.path.join(log_dir, "fashion_mnist.h5")

    callbacks = [
        keras.callbacks.TensorBoard(log_dir),
        keras.callbacks.ModelCheckpoint(ouput_model_file, save_best_only=True),
        keras.callbacks.EarlyStopping(patience=5, min_delta=1e-3),
    ]
    history = models.fit(x_train_scaled, y_train, epochs=20, validation_data=(x_valid_scaled, y_valid),
                         callbacks=callbacks)

    # 测试集上评估
    print(models.evaluate(x_test_scaled, y_test))

    # 存储训练过程中的一些值  如损失 accury等
    print(history.history)

    pd.DataFrame(history.history).plot(figsize=(8, 5))
    plt.grid(True)
    plt.gca().set_ylim(0, 1)
    plt.show()


if __name__ == '__main__':
    train()
    # show_single_image(x_train[0])
    # show_images(10,5,x_train,y_train,class_names)
