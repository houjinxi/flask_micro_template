# -*- coding: utf-8 -*-
""" 框架数据库配置 """
from app.main.extensions import env
from app.main.settings.config_center import ConfigCenterConfig
from app.main.settings.default import Config

TYPE = env.str("CONFIG_TYPE", default="local")
ENV = env.str("FLASK_ENV", default="prod")

""" 环境配置说明
提供三种方式定义框架配置：
1.环境变量配置
2.环境配置文件.env/.flaskenv
3.环境配置选项器config_option：本地(local)/读取配置中心配置(remote)

数据库选项:
1.sqlite3
2.mysql

"""


class DevelopmentConfig(Config):
    LOG_LEVEL = "debug"


class TestingConfig(Config):
    DEBUG = True
    LOG_LEVEL = "info"
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = "error"


config = {
    "0": {  # local：本地配置
        "dev": DevelopmentConfig,
        "test": TestingConfig,
        "prod": ProductionConfig
    }[ENV],
    "1": ConfigCenterConfig,  # remote：远程调用配置中心
}[TYPE]
