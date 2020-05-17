# -*- coding: utf-8 -*-
""" 初始化 app ，并加载路由、数据库配置、日志、其他拓展等"""
import logging
import sys
from logging.handlers import RotatingFileHandler  # 日志处理
from flask import Flask, render_template  # render_template 模板渲染
from flask.logging import default_handler  # fast_api
from app.general import commands  # 命令行执行
from app.main.settings import config  # 加载配置
from app.main.routers import blueprint  # 蓝图，flask blueprint,不同蓝本分为不同模块，然后可以相互调用
from app.main.extensions import (
    cache,
    db,
    debug_toolbar,
    # csrf_protect,
    flask_bcrypt,
    flask_static_digest,
    login_manager,
    cors, migrate
)


def create_app(config_object=config):  # 注册模块
    """Create application factory, as explained here: http://flask.pocoo.org/docs/core/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    configure_logger(app)
    register_commands(app)
    # fix_flask_restplus()
    return app


def register_extensions(app):
    """Register Flask extensions."""
    flask_bcrypt.init_app(app)
    cache.init_app(app)
    db_init(app)
    migrate.init_app(app, db)
    # csrf_protect.init_app(app)
    cors.init_app(app, supports_credentials=True)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    flask_static_digest.init_app(app)


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(blueprint)
    return None


def register_commands(app):
    """Register Click commands."""
    for name, value in vars(commands).items():
        if value.__class__.__name__ == 'Command':
            app.cli.add_command(value)


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template(f"{error_code}.html"), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def configure_logger(app):
    """Configure system loggers.
    Keep the flask Version 1.1.1 or above
    """

    # Remove the default handler.
    app.logger.removeHandler(default_handler)
    formatter = logging.Formatter(
        "[%(asctime)s]-[%(thread)d:%(threadName)s]-[%(filename)s:%(module)s:%(funcName)s]-"
        "[%(levelname)s]-%(message)s"
    )
    # Create the log file atomically.Set the log file size to 50MB.1 MB = 1024 * 1024 bytes.
    # If it exceeds 50MB, the new log file will be written automatically and the historical file will be archived.
    file_handler = RotatingFileHandler(
        filename=app.config["LOG_FILENAME"],
        mode="a",
        maxBytes=50 * 1024 * 1024,
        backupCount=10,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.INFO)
    for logger in (
            # More log modules can be added here.For details, please refer to the official documentation of flask:
            # https://flask.palletsprojects.com/en/1.0.x/logging/
            app.logger,
            logging.getLogger("sqlalchemy"),
            logging.getLogger("werkzeug"),
    ):
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)


def db_init(app):  # 初始化db,并创建models中定义的表格
    with app.app_context():  # 添加这一句，否则会报数据库找不到application和context错误
        db.init_app(app)  # 初始化db
        db.create_all()  # 创建所有未创建的table


def fix_flask_restplus():  # 由于flask_restplus后续没有维护了，内含导入的werkzeug包需要修改
    for name in ["fields", "api"]:
        site_packages = [path for path in sys.path if "site-packages" == path[-13:]][0]
        path = f"{site_packages}/flask_restplus/{name}.py"
        if path:
            with open(path, 'r', encoding='utf-8') as read_py_file:
                old = "from werkzeug import cached_property"
                new = "from werkzeug.utils import cached_property"
                content = read_py_file.read().replace(old, new)
            with open(path, 'w', encoding='utf-8') as write_py_file:
                write_py_file.write(content)
