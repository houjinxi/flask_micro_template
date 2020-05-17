# -*- coding: utf-8 -*-
import time
from app.main.extensions import env, root_dir

""" Log File """
log_path = root_dir / 'logs'
log_path.mkdir(parents=True, exist_ok=True)
DATABASE = env.str("DATABASE", default="sqlite3")
DATABASE = "sqlite3" if DATABASE not in ["sqlite3", "mysql"] else DATABASE


# 数据库配置
class Sqlite3Config:  # sqlite3
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{root_dir}/sqlite3.db"


class MysqlConfig:  # Mysql 数据库 flask_sqlalchemy
    DIALECT = "mysql"
    DRIVER = "pymysql"
    USERNAME = "root"
    PASSWORD = "123456"
    HOST = "127.0.0.1"
    PORT = "3306"
    DATABASE = "flask_micro_framework"

    SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(
        DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE
    )
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_MAX_OVERFLOW = 5


class Config(dict(sqlite3=Sqlite3Config, mysql=MysqlConfig)[DATABASE]):
    SECRET_KEY = "*7k6q9!~19^*&1*6&23(@74a&^f3asd>&^$"
    DEBUG = True
    CSRF_ENABLED = True
    DEBUG_TB_ENABLED = DEBUG

    LOG_FILENAME = log_path / f"{time.strftime('%Y-%m-%d', time.localtime(time.time()))}.log"
    LOG_LEVEL = 'info'

    SQLALCHEMY_BINDS = None
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    ENABLE_SENTRY = False
    SENTRY_DSN = ''
    SEND_FILE_MAX_AGE_DEFAULT = 0
    BCRYPT_LOG_ROUNDS = 13

    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = "simple"  # Can be "memcached", "redis", etc.


if __name__ == '__main__':
    print()
