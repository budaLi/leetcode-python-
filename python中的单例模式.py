#-*-coding:utf8-*-
#author : Lenovo
#date: 2018/9/14
class Single(object):
    _instance=None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance=super(Single, cls).__new__(cls, *args, **kwargs)
        return cls._instance

