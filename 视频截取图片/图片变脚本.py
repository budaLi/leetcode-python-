# @Time    : 2020/5/28 14:25
# @Author  : Libuda
# @FileName: 图片变脚本.py
# @Software: PyCharm
# -*- coding: utf-8 -*-
"""以python模块形式存储、使用二进制文件"""
import os
import base64
from io import BytesIO


def bin2module(bin_file, py_file=None):
    """二进制文件转存为python模块
    bin_file  - 二进制文件名
    py_file   - 生成的模块文件名，默认使用二进制文件名，仅更改后缀名
    """
    fpath, fname = os.path.split(bin_file)
    fn, ext = os.path.splitext(fname)
    if not py_file:
        py_file = os.path.join(fpath, '%s.py' % fn)
    with open(bin_file, 'rb') as fp:
        content = fp.read()
    content = base64.b64encode(content)
    content = content.decode('utf8')
    with open(py_file, 'w') as fp:
        fp.write('content = """%s"""\n\n' % content)


if __name__ == '__main__':
    """测试代码"""
    # 将图像文件转存为img_demo.py
    bin2module('0_51_Dresses_wearingdress_51_377_0.png', 'demo.py')
    # 导入刚刚生成的demo模块
    import demo
    # 用pillow打开图像，验证demo模块的get_fp()：返回二进制的IO对象（类文件对象）
    from PIL import Image

    im = Image.open(demo.get_fp())
    im.show()
    # 保存为本地文件，验证demo模块的save()：保存文件
    demo.save('demo_save.png')
