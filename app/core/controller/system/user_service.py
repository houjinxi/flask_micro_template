# -*- coding: utf-8 -*-
# @Time    : 2020/3/4 16:35
# @Author  : HoxHou
# @File    : user_service.py
# @Software: PyCharm
# When I wrote this, only God and I understood what I was doing
# Now, God only knows


from app.core.model.system.user import User
from app.main.extensions import logs
from app.general.response import MsgBody

# 初始化消息体


msg = MsgBody()
# 响应码
CONFLICT = msg.code("CONFLICT")
CREATED = msg.code("CREATED")
UNAUTHORIZED = msg.code("UNAUTHORIZED")


class SysUserController:
    """ 系统用户控制器 """

    @logs.catch()
    def get_all_users(self):
        return User.query.all()

    @logs.catch()
    def get_a_user(self, public_id):
        return User.query.filter_by(public_id=public_id).first()

    @logs.catch()
    def create_user(self, data):
        """ 新增用户 """
        user = User.query.filter_by(phone=data["phone"]).first()  # 判断是否新增:身份唯一性
        if not user:
            new_user = User.create(**data)  # 创建新用户
            return self.generate_token(new_user)  # 生成Token
        else:  # 用户已存在
            msg.set_msg(
                code=CONFLICT,
                msg="User already exists. Please Log in.",
                data=user.user_name,
            )
            return msg.body

    @staticmethod
    def generate_token(user):
        """ token 生成器 """
        try:  # generate the auth token
            auth_token = User.encode_auth_token(user.id)  # token编码
            data = dict(Authorization=auth_token.decode())
            msg.set_msg(code=CREATED, msg="Successfully registered.", data=data)
            return msg.body
        except Exception as e:
            logs.debug(e)
            msg.set_msg(code=UNAUTHORIZED, msg="Some error occurred. Please try again.")
            return msg.body


if __name__ == "__main__":
    sys = SysUserController()
    result = sys.create_user(
        {
            "user_name": "test1",
            "password": "123456",
            "phone": "13410319559",
            "email": "string",
        }
    )
    print(result)
