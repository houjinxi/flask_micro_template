# -*- coding: utf-8 -*-
# @Time    : 2020/5/17 17:24
# @Author  : HoxHou
# @File    : edit_site_packages.py
# @Software: PyCharm
# When I wrote this, only God and I understood what I was doing
# Now, God only knows

import sys


def site_packages_address():  # 读取site-packages路径
    return [path for path in sys.path if "site-packages" == path[-13:]]


if __name__ == '__main__':
    print(site_packages_address())
