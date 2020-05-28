# @Time    : 2020/5/28 14:20
# @Author  : Libuda
# @FileName: 视频变图片帧.py
# @Software: PyCharm

import argparse
import os

import cv2


def parse_args():
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser(description='Process pic')
    parser.add_argument('--input', help='video to process', dest='input',
                        default="38f98723f3525f0518537c1d36677cf1.mp4", type=str)
    parser.add_argument('--output', help='pic to store', dest='output', default="./imgs", type=str)
    # default为间隔多少帧截取一张图片
    parser.add_argument('--skip_frame', dest='skip_frame', help='skip number of video', default=1,
                        type=int)  # 此处可更改提取帧的间隔
    args = parser.parse_args()  # 此处添加路径，input为输入视频的路径 ，output为输出存放图片的路径
    return args


def process_video(i_video, o_video, num):
    cap = cv2.VideoCapture(i_video)
    num_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    expand_name = '.png'
    if not cap.isOpened():
        print("Please check the path.")
    cnt = 0
    count = 0
    while 1:
        ret, frame = cap.read()
        cnt += 1
        # how
        # many
        # frame
        # to
        # cut
        if cnt % num == 0:
            count += 1
            print(frame)
            frame = cv2.resize(frame, (128, 128))
            cv2.imwrite(os.path.join(o_video, "shimei" + str(count) + expand_name), frame)
        if not ret:
            break


if __name__ == '__main__':
    args = parse_args()
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    print('Called with args:')
    print(args)
    process_video(args.input, args.output, args.skip_frame)
