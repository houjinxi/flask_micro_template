# -*- coding: utf-8 -*-
""" 读取配置中心配置"""


def remote_config():
    return {"SECRET_KEY": ""}


class ConfigCenterConfig:
    RemoteConfig = remote_config()
    SECRET_KEY = RemoteConfig["SECRET_KEY"]
