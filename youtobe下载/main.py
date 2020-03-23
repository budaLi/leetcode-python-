# @Time    : 2019/12/17 9:24
# @Author  : Libuda
# @FileName: 远程服务器文件监控.py
# @Software: PyCharm
import subprocess


# 下载视频函数
def down_videos(url):
    urls = r'C:\Users\lenovo\Desktop\开发\youtube-dl.exe {} % '.format(url)
    p = subprocess.Popen(urls, shell=True, universal_newlines=True)
    p.wait()  # 阻塞，等待子进程完成
    print('------>', p.returncode)  # 判断执行状态，成功返回0


if __name__ == '__main__':
    down_videos("https://www.youtube.com/watch?v=4UP-p3ZP5cA")
