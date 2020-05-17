# -*- coding: utf-8 -*-
# @Time    : 2020/3/4 9:23
# @Author  : HoxHou
# @File    : user_dto.py
# @Software: PyCharm
# When I wrote this, only God and I understood what I was doing
# Now, God only knows
from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace("user", description="user related operations")
    user = api.model(
        "user",
        {
            "user_name": fields.String(required=True, description="user username"),
            "password": fields.String(required=True, description="user password"),
            "phone": fields.String(
                required=True, description="user phone", max_length=11
            ),
            "email": fields.String(required=False, description="user email address"),
        },
    )
