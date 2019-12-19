# -*-coding:utf8-*-
# author : Lenovo
# date: 2018/9/6
import os
import sys
from contextlib import closing  # 把任意对象变为上下文管理 并支持with语句
import requests
from tqdm import tqdm

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings()


def video_downloader(vedio_path, vedio_name, video_url):
    print('下载链接', video_url)
    sess = requests.Session()
    size = 0

    with closing(sess.get(video_url, stream=True, verify=False)) as response:
        chunk_size = 1024
        content_size = int(response.headers['content-length'])
        if response.status_code == 200:
            sys.stdout.write('[文件大小]:%0.2f MB\n' % (content_size / chunk_size / 1024))
            video_name = os.path.join(vedio_path, vedio_name)

            with open(video_name, 'wb') as file:
                for data in tqdm(response.iter_content(chunk_size=chunk_size)):
                    file.write(data)
                    size += len(data)
                    # sys.stdout.write('[下载进度]:%.2f%%' % float(size / content_size * 100) + '\r')
                    # sys.stdout.flush()
                    # if size / content_size == 1:
                    #     print('\n')
            print("下载完成")
        else:
            print('链接异常')


if __name__ == "__main__":
    vedio_path = r'C:\Users\lenovo\PycharmProjects\leetcode-python-\视频下载脚本'
    flag = True
    i = 1
    while flag:
        vedio_name = "{}.ts".format(i)
        url = 'https://xuecdn2.aliyunedu.net/courselesson-22/20190606022823-ge16f2o98fcokoos-conv/e_20190606022823-ge16f2o98fcokoos-conv_hd_seg_{}.ts'.format(
            i)
        video_downloader(vedio_path, vedio_name, url)
        i += 1
