# -*- coding: utf-8 -*-
# @Time    : 2020/3/4 9:24
# @Author  : HoxHou
# @File    : auth_dto.py
# @Software: PyCharm
# When I wrote this, only God and I understood what I was doing
# Now, God only knows
from flask_restplus import Namespace, fields


class AuthDto:
    api = Namespace("auth", description="authentication related operations")
    user_auth = api.model(
        "auth_details",
        {
            "phone": fields.String(required=True, description="The phone"),
            "password": fields.String(required=True, description="The user password "),
        },
    )
