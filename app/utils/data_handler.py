# -*- coding: utf-8 -*-
# @Time    : 2020/3/2 17:21
# @Author  : HoxHou
# @File    : data_handler.py
# @Software: PyCharm
# When I wrote this, only God and I understood what I was doing
# Now, God only knows


import collections


class DataChecker(object):
    def __init__(self):
        pass

    @staticmethod
    def option(*args, **kwargs):
        return Extend(*args, **kwargs)


class Extend(object):
    def __init__(self, data):
        self.value = data

    @property
    def is_empty(self):
        return not self.value and isinstance(self.value, collections.Iterable)
