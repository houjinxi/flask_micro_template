# -*- coding: utf-8 -*-
# @Time    : 2020/3/3 9:06
# @Author  : HoxHou
# @File    : response_msg.py
# @Software: PyCharm
# When I wrote this, only God and I understood what I was doing
# Now, God only knows
from typing import Union

from app.main.extensions import env
from app.utils.params_type import type_interceptor


class MsgBody(object):
    def __init__(self):
        """ 默认消息体"""
        self.msg = dict(code=None, msg=None, data=None)

    @staticmethod
    def code(env_msg):  # 系统响应码
        return env.str(env_msg)

    def __built_in(self, code=None, msg=None, data=None, ext_fields=None):
        """ 内建方法 """
        self.msg.update(
            {
                "code": code or self.msg.get("code"),
                "msg": msg or self.msg.get("msg"),
                "data": data or self.msg.get("data"),
            }
        )
        if ext_fields:
            self.msg.update(ext_fields)
        return self.msg

    @type_interceptor()
    def set_msg(
        self,
        code: Union[int, str] = None,
        msg: str = None,
        data: Union[dict, str, None] = None,
    ):
        """ 设置消息体 """
        self.__built_in(code=code, msg=msg, data=data)

    def add_fields(self, **kwargs):
        """ 新增字段 """
        self.__built_in(ext_fields=kwargs)

    @property
    def body(self):
        """ 响应消息体 """
        temp = self.__built_in()
        code = temp.get("code") or self.code("MEESAGE")
        msg = temp.get("msg") or "响应消息体"
        return self.__built_in(code=code, msg=msg), int(code[:3])


if __name__ == "__main__":
    remsg = MsgBody()
    remsg.set_msg(
        code="442", msg="234433",
    )
    # remsg.add_fields(dsss={"dsf": "333"})
    print(remsg.body)
