# -*- coding: utf-8 -*-
# @Time    : 2020/3/19 10:45
# @Author  : HoxHou
# @File    : path_libs.py
# @Software: PyCharm
# When I wrote this, only God and I understood what I was doing
# Now, God only knows
from pathlib import *

# 获取当前路径
path = Path().cwd()
# print(path)
# path = Path(path)
# # 返回路径字符串中所包含的各部分
# print(path.parts)
# # 返回路径字符串中的驱动器盘符
# print(path.drive)
# # 返回路径字符串中的根路径
# print(path.root)
# # 返回路径字符串中的盘符和根路径
# print(path.anchor)
# # 返回当前路径的全部父路径
# print(path.parents)
# # 返回当前路径的上一级路径
# print(path.parent)
# print(path.parents[0])  # 获取某一父路径
# # 返回当前路径中的文件名
# print(path.name)
# # 返回当前路径中的文件所有后缀名
# print(Path(path, 'app.py').suffixes)
# # 返回当前路径中的文件后缀名
# print(Path(path, 'app.py').suffix)
# print(Path(path, 'app.py').suffixes[0])  # 获取某一文件后缀
# # 返回当前路径中的主文件名
# print(path.stem)
# # 将当前路径转换成 UNIX 风格的路径
# print(path.as_posix())
# # 将当前路径转换成 URL。只有绝对路径才能转换，否则将会引发 ValueError
# print(path.as_uri())
# # 判断当前路径是否为绝对路径
# print(path.is_absolute())
# # 将多个路径连接在一起，作用类似于前面介绍的斜杠（/）连接符
# print(path.joinpath('aa', 'bb', 'cc'))
# print(Path(path, 'aa', 'bb', 'cc'))  # 以上等效方法
# # 判断当前路径是否匹配指定通配符
# print(Path(path, 'app.py').match('*.py'))
# # 将当前路径中的文件名替换成新文件名,非真实替换
# print(path.with_name('ss'))
# # 将当前路径中的文件后缀名替换成新的后缀名。如果当前路径中没有后缀名，则会添加新的后缀名
# print(path.with_suffix('.py'))
# # 获取当前文件和文件夹的元信息
# print(path.stat().st_size)
# # 修改路径目录或文件权限
# Path().chmod(0o444)

# Path().mkdir()