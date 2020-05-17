from functools import wraps
from flask import request
from app.core.controller.system.auth_service import SysAuthController
from app.main.extensions import login_manager

sys_auth = SysAuthController()
"""
框架鉴权
"""


@login_manager.user_loader
def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        data, status = sys_auth.get_logged_in_user(request)
        token = data.get("data")

        if not token:
            return data, status

        return func(*args, **kwargs)

    return decorated


def admin_token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):

        data, status = sys_auth.get_logged_in_user(request)
        token = data.get("data")

        if not token:
            return data, status

        admin = token.get("is_admin")  # 判断是否系统管理员
        if not admin:
            response_object = {"status": "fail", "message": "admin token required"}
            return response_object, 401

        return func(*args, **kwargs)

    return decorated
