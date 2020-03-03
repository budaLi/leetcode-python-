# @Time    : 2020/3/3 20:43
# @Author  : Libuda
# @FileName: config.py
# @Software: PyCharm
from configparser import ConfigParser

config_parser = ConfigParser()
config_parser.read('config.cfg', encoding="utf-8-sig")
config = config_parser['default']


def get_config():
    return config
