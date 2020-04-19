# @Time    : 2020/4/14 11:32
# @Author  : Libuda
# @FileName: mian.py
# @Software: PyCharm
import numpy as np
import imgaug.augmenters as iaa
import cv2
import imageio
import imgaug as ia
import matplotlib.pyplot as plt


def test1():
    images = np.zeros((2, 128, 128, 3), dtype=np.uint8)  # two example images
    images[:, 64, 64, :] = 255
    points = [
        [(10.5, 20.5)],  # points on first image
        [(50.5, 50.5), (60.5, 60.5), (70.5, 70.5)]  # points on second image
    ]

    seq = iaa.Sequential([
        iaa.AdditiveGaussianNoise(scale=0.05 * 255),
        iaa.Affine(translate_px={"x": (1, 5)})
    ])

    # augment keypoints and images
    images_aug, points_aug = seq(images=images, keypoints=points)

    print("Image 1 center", np.argmax(images_aug[0, 64, 64:64 + 6, 0]))
    print("Image 2 center", np.argmax(images_aug[1, 64, 64:64 + 6, 0]))
    print("Points 1", points_aug[0])
    print("Points 2", points_aug[1])


def test2():
    image = imageio.imread("http://wx4.sinaimg.cn/large/006HcH9cgy1g2ywu5fooxj30oy0gimz1.jpg")  # 读取图片数据

    seq = iaa.Sequential([  # 定义一个sequential，把要进行的图片操作（3个操作）放在里面
        iaa.Affine(rotate=(-25, 25)),
        iaa.AdditiveGaussianNoise(scale=(10, 30)),
        iaa.Crop(percent=(0, 0.4))
    ], random_order=True)  # 这3个图片操作以随机顺序作用在图片上

    images_aug = [seq.augment_image(image) for _ in range(8)]  # 应用data augmentation
    ia.imshow(ia.draw_grid(images_aug, cols=4, rows=2))  # 显示图片操作效果

    # for index, one in enumerate(images_aug):
    #     cv2.imwrite(str(index) + ".jpg", one)


def test3():
    file_list = "list"
    with open(file_list, 'r') as f:
        lines = f.readlines()[:1]
    for line in lines:
        line = line.strip().split()
        path = line[0]
        landmark = line[1:197]
        attribute = line[197:203]
        euler_angle = line[203:206]

        image = imageio.imread("http://wx4.sinaimg.cn/large/006HcH9cgy1g2ywu5fooxj30oy0gimz1.jpg")  # 读取图片数据
        # ia.imshow(image)

        keypoints = ia.KeypointsOnImage([
            ia.Keypoint(x=65, y=100),
            ia.Keypoint(x=75, y=200),
            ia.Keypoint(x=100, y=100),
            ia.Keypoint(x=200, y=80)
        ], shape=image.shape)

        # landmark = np.asarray(landmark, dtype=np.float32)

        seq = iaa.Sequential([  # 定义一个sequential，把要进行的图片操作（3个操作）放在里面
            iaa.Affine(rotate=(-20, 20)),
            # iaa.AdditiveGaussianNoise(scale=(10, 30)),
            # iaa.Crop(percent=(0, 0.4))
        ], random_order=True)  # 这3个图片操作以随机顺序作用在图片上

        # augment keypoints and images
        images_aug, points_aug = seq(images=image, keypoints=keypoints)

        # images_aug = [seq.augment_image(image) for _ in range(8)]  # 应用data augmentation

        # for index,one in enumerate(images_aug):
        #     cv2.imwrite(str(index)+".jpg",one)
        # images_aug,points_aug = [seq(images=image, keypoints=keypoints) for _ in range(8)]  # 应用data augmentation

        ia.imshow(images_aug)  # 显示图片操作效果


def test4():
    # image = ia.quokka(size=(256, 256))
    file_list = "list"
    with open(file_list, 'r') as f:
        lines = f.readlines()[:1]
    landmarks = []
    for line in lines:
        line = line.strip().split()
        path = line[0]
        landmark = line[1:197]
        attribute = line[197:203]
        euler_angle = line[203:206]

        image = imageio.imread(path)  # 读取图片数据

        h, w, _ = image.shape

        # 定义关键点
        landmark = np.asarray(landmark, dtype=np.float32)

        lad_ls = []

        # 变成绝对位置
        for x, y in landmark.reshape(-1, 2) * [h, w]:
            lad_ls.append(ia.Keypoint(x, y))

        # 相对位置
        # for x,y in landmark.reshape(-1, 2):
        #     lad_ls.append(ia.Keypoint(x,y))

        keypoints = ia.KeypointsOnImage(lad_ls, shape=image.shape)

        # 定义一个变换序列
        seq = iaa.Sequential([
            iaa.Multiply((1.2, 1.5)),  # 改变亮度,不影响关键点
            iaa.Affine(
                rotate=(-20, 20),
                # scale=(0.7, 0.9)  # 旋转10度然后缩放,会影响关键点
            ),
            # iaa.Fliplr(0.5),
            iaa.GaussianBlur(sigma=(0, 3.0)),
            # iaa.Crop(percent=(0, 0.4))
        ], random_order=True)

        # 固定变换序列,之后就可以先变换图像然后变换关键点,这样可以保证两次的变换完全相同。
        # 如果调用次函数,需要在每次batch的时候都调用一次,否则不同的batch执行相同的变换。
        seq_det = seq.to_deterministic()

        # 转换成list或者batch来变换。由于只有一张图片, 因此用[0]来取出该图和关键点。
        image_aug = seq_det.augment_images([image])[0]
        keypoints_aug = seq_det.augment_keypoints([keypoints])[0]

        # print coordinates before/after augmentation (see below)
        # use after.x_int and after.y_int to get rounded integer coordinates
        for i in range(len(keypoints.keypoints)):
            before = keypoints.keypoints[i]
            before = keypoints.get_coords_array() / 112
            after = keypoints_aug.keypoints[i]
            after = keypoints_aug.get_coords_array() / 112
            # after_new = keypoints_aug.get_coords_array()
            print("Keypoint %d:   (%.16f, %.16f) ->  (%.16f, %.16f)" % (
                i, before[i][0], before[i][1], after[i][0], after[i][1])
                  )

        # keypoints = keypoints.get_coords_array()*[h,w]
        # keypoints = ia.KeypointsOnImage.from_coords_array(keypoints,image.shape)
        #
        # keypoints_aug = keypoints_aug.get_coords_array()*[h,w]
        # keypoints_aug = ia.KeypointsOnImage.from_coords_array(keypoints_aug,image.shape)
        # 将关键点画在图片上。
        # image with keypoints before/after augmentation (shown below)
        image_before = keypoints.draw_on_image(image, size=1)
        image_after = keypoints_aug.draw_on_image(image_aug, size=1)

        fig, axes = plt.subplots(2, 1, figsize=(20, 15))
        plt.subplots_adjust(left=0.2, bottom=0.2, right=0.8, top=0.8, hspace=0.3, wspace=0.0)
        axes[0].set_title("image before")
        axes[0].imshow(image_before)
        axes[1].set_title("image after augmentation")
        axes[1].imshow(image_after)

        plt.show()

        # 增强n次 后显示图片
        # images_aug = [seq.augment_image(image) for _ in range(8)]  # 应用data augmentation
        # ia.imshow(ia.draw_grid(images_aug, cols=4, rows=2))  # 显示图片操作效果


if __name__ == '__main__':
    import time

    for i in range(10):
        test4()
        time.sleep(5)
