from flask import request
from flask_restplus import Resource
from app.core.controller.system.auth_service import SysAuthController
from app.main.dto.system.auth_dto import AuthDto

# Dto Layer
auth_dto_api = AuthDto.api
user_auth = AuthDto.user_auth
# Control Layer
sys_auth = SysAuthController()


@auth_dto_api.route("/token")
class LoginToken(Resource):
    """ User Login Token """

    @auth_dto_api.doc("login token")
    def post(self):
        # from data
        user_info = request.form.to_dict()
        return sys_auth.create_token(data=user_info)


@auth_dto_api.route("/login")
class UserLogin(Resource):
    """ User Login Resource """

    @auth_dto_api.doc("user login")
    @auth_dto_api.expect(user_auth, validate=True)
    def post(self):
        # get the post data
        return sys_auth.login(data=request.json)


@auth_dto_api.route("/logout")
class LogoutAPI(Resource):
    """ Logout Resource """

    @auth_dto_api.doc("logout a user")
    def post(self):
        # get auth token
        auth_header = request.headers.get("Authorization")
        return sys_auth.logout(data=auth_header)
