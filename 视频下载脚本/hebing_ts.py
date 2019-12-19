# @Time    : 2019/12/19 13:02
# @Author  : Libuda
# @FileName: hebing_ts.py
# @Software: PyCharm
from moviepy.editor import VideoFileClip, concatenate
from moviepy.video.io.VideoFileClip import VideoFileClip
from natsort import natsorted
import os


def hebin(mp4_path, target_path):
    # 定义一个数组
    L = []

    # 访问 video 文件夹 (假设视频都放在这里面)
    for root, dirs, files in os.walk(mp4_path):
        # 按文件名排序
        files = natsorted(files)
        # 遍历所有文件
        print(files)
        for file in files:
            # 如果后缀名为 .mp4
            if file.split(".")[1] == 'ts':
                # 拼接成完整路径
                filePath = os.path.join(root, file)
                print(filePath)
                # 载入视频
                video = VideoFileClip(filePath)
                print(video)
                # 添加到数组
                L.append(video)

    # 拼接视频
    final_clip = concatenate(L)

    # 生成目标视频文件
    final_clip.to_videofile(target_path + '.mp4', fps=24, remove_temp=False)


if __name__ == '__main__':
    ts_path = r"C:\Users\lenovo\PycharmProjects\leetcode-python-\视频下载脚本"
    tag = r'C:\Users\lenovo\PycharmProjects\leetcode-python-\视频下载脚本'
    hebin(ts_path, tag)
