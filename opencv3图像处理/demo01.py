# @Time    : 2020/4/8 14:41
# @Author  : Libuda
# @FileName: demo01.py
# @Software: PyCharm
import cv2 as cv
import time

img_path = "test.jpg"


def op_image():
    src = cv.imread(img_path)

    # 图像分辨率和色彩通道  (1920, 1080, 3)
    print(src.shape)
    # 图片大小 字节  6220800 (1920 x 1080 x 3)
    print(src.size)

    # 每个像素三通道 数据类型
    print(src.dtype)

    # cv.namedWindow("my pic",cv.WINDOW_FULLSCREEN)

    cv.imshow("img", src)

    cv.waitKey(0)

    cv.destroyAllWindows()


def op_vedio():
    # 多个摄像头 索引
    capture = cv.VideoCapture(0)

    while 1:
        # frame 图片的每一帧
        ret, frame = capture.read()
        # 镜像调换 上下 1 为正
        frame = cv.flip(frame, -1)
        cv.imshow("video", frame)
        c = cv.waitKey(50)

        # esc退出
        if c == 27:
            break


def get_op_time():
    t1 = cv.getTickCount()
    import time
    time.sleep(3)
    t2 = cv.getTickCount()

    time = (t2 - t1) / cv.getTickFrequency()

    print(time)


if __name__ == '__main__':
    # op_vedio()
    get_op_time()
