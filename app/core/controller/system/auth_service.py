# -*- coding: utf-8 -*-
# @Time    : 2020/3/5 10:04
# @Author  : HoxHou
# @File    : auth_service.py
# @Software: PyCharm
# When I wrote this, only God and I understood what I was doing
# Now, God only knows
from app.core.model.system.blacklist import BlacklistToken
from app.core.model.system.user import User
from app.main.extensions import logs
from app.general.response import MsgBody

# 初始化消息体
msg = MsgBody()
# 响应码
SUCCESS = msg.code("SUCCESS")
CONFLICT = msg.code("CONFLICT")
UNAUTHORIZED = msg.code("UNAUTHORIZED")
INTERNAL_SERVER_ERROR = msg.code("INTERNAL_SERVER_ERROR")
FORBIDDEN = msg.code("FORBIDDEN")


class SysAuthController:
    """ 系统鉴权 """

    @staticmethod
    def save_token(token):
        try:  # insert the token
            BlacklistToken.create(token=token)
            msg.set_msg(code=SUCCESS, msg="Successfully logged out.")
        except Exception as e:
            msg.set_msg(code=INTERNAL_SERVER_ERROR, msg=str(e))
        return msg.body

    @staticmethod
    def create_token(data):  # 登录校验
        try:  # fetch the user data
            user = User.query.filter_by(phone=data["username"]).first()  # 判断身份唯一性
            if user and user.check_password(data.get("password")):  # 校验用户密码
                auth_token = User.encode_auth_token(user.id)
                if auth_token:  # 校验通过
                    success = MsgBody()  # 初始化响应消息
                    success.set_msg(
                        code=SUCCESS, msg="Successfully logged in."
                    )
                    success.add_fields(access_token=auth_token.decode(), token_type="bearer")  # access_token
                    return success.body
            else:
                msg.set_msg(code=UNAUTHORIZED, msg="phone or password does not match.")
        except Exception as e:
            logs.error(e)
            msg.set_msg(code=INTERNAL_SERVER_ERROR, msg="Try again")
        return msg.body

    @staticmethod
    def login(data):  # 登录校验
        try:  # fetch the user data
            user = User.query.filter_by(phone=data["phone"]).first()  # 判断身份唯一性
            if user and user.check_password(data.get("password")):  # 校验用户密码
                auth_token = User.encode_auth_token(user.id)
                if auth_token:  # 校验通过
                    success = MsgBody()  # 初始化响应消息
                    data = dict(Authorization=auth_token.decode())
                    success.set_msg(
                        code=SUCCESS, msg="Successfully logged in.", data=data
                    )
                    return success.body
            else:
                msg.set_msg(code=UNAUTHORIZED, msg="phone or password does not match.")
        except Exception as e:
            logs.error(e)
            msg.set_msg(code=INTERNAL_SERVER_ERROR, msg="Try again")
        return msg.body

    @logs.catch()
    def logout(self, data):
        auth_token = "" or data
        if auth_token:
            resp = User.decode_auth_token(auth_token)  # 判断token是否在黑名单
            if not isinstance(resp, str):  # mark the token as blacklisted
                return self.save_token(token=auth_token)  # 退出登录后自动加入黑名单，销毁Token
            else:
                msg.set_msg(code=UNAUTHORIZED, msg=resp)
        else:
            msg.set_msg(code=FORBIDDEN, msg="Provide a valid auth token.")
        return msg.body

    @staticmethod
    @logs.catch()
    def get_user_permission(request=None):
        """
        1.权限查询
        2.等级查询
        可拓展为：接口权限、方法权限、查询权限
        role 角色表
        :param request:
        :return:
        """
        auth_token = request.headers.get('Authorization')  # get the auth token
        if auth_token:
            resp = User.decode_auth_token(auth_token[7:])  # Token解码
            if not isinstance(resp, str):  # 查询成功会返回int类型
                user = User.query.filter_by(id=resp).first()
                success = MsgBody()  # 初始化响应消息
                data = dict(user_id=user.id, email=user.email, is_admin=user.is_admin)
                success.set_msg(code=SUCCESS, msg="The query is successful.", data=data)
                return success.body
            msg.set_msg(code=UNAUTHORIZED, msg=resp)
        else:
            msg.set_msg(code=UNAUTHORIZED, msg="Provide a valid auth token.")
        return msg.body

    @staticmethod
    def get_logged_in_user(new_request):
        auth_token = new_request.headers.get("Authorization")  # get the auth token
        if auth_token:
            resp = User.decode_auth_token(auth_token[7:])
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                response_object = {
                    "status": "success",
                    "data": {
                        "user_id": user.id,
                        "email": user.email,
                        # "is_admin": user.is_admin,
                        # 'registered_on': str(user.registered_on)
                    },
                }
                return response_object, 200
            response_object = {"status": "fail", "message": resp}
            return response_object, 401
        else:
            response_object = {
                "status": "fail",
                "message": "Provide a valid auth token.",
            }
            return response_object, 401
