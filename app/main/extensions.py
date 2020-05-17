# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the core factory located in core.py."""
from pathlib import Path
from environs import Env
from flask_bcrypt import Bcrypt
from flask_caching import Cache  # 减少缓存穿透，给需要已经时间才能获取结果和不需要频繁更新的视图提供缓存服务
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # Flask应用处理SQLAlchemy数据库迁移的扩展 数据库迁移
from flask_static_digest import FlaskStaticDigest
from loguru import logger  # 日志输出框架使用
from flask_cors import CORS  # 解决跨域请求的问题

# from flask_wtf.csrf import CSRFProtect

""" Factory Function """
flask_bcrypt = Bcrypt()
# csrf_protect = CSRFProtect()
login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
cache = Cache()
debug_toolbar = DebugToolbarExtension()
flask_static_digest = FlaskStaticDigest()
env = Env()
env.read_env()
logs = logger
cors = CORS()
root_dir = Path().resolve()  # 系统路径
