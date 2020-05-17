from flask import request
from flask_restplus import Resource
from app.core.controller.system.user_service import SysUserController
from app.main.dto.system.user_dto import UserDto
from app.general.decorator import token_required

# Dto Layer
user_dto_api = UserDto.api
_user = UserDto.user
# Control Layer
controller = SysUserController()


@user_dto_api.route("/")
class UserList(Resource):
    @user_dto_api.doc("list_of_registered_users")
    @token_required
    @user_dto_api.marshal_list_with(_user, envelope="data")
    def get(self):
        """List all registered users"""
        return controller.get_all_users()

    @user_dto_api.expect(_user, validate=True)
    @user_dto_api.response(201, "User successfully created.")
    @user_dto_api.doc("create a new user")
    def post(self):
        """Creates a new User """
        return controller.create_user(data=request.json)


@user_dto_api.route("/<public_id>")
@user_dto_api.param("public_id", "The User identifier")
@user_dto_api.response(404, "User not found.")
class User(Resource):
    @user_dto_api.doc("get a user")
    @user_dto_api.marshal_with(_user)
    def get(self, public_id):
        """get a user given its identifier"""
        user = controller.get_a_user(public_id)
        if not user:
            user_dto_api.abort(404)
        else:
            return user
