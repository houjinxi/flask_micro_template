""" Routers of the blueprint is use to create name space"""
from flask import Blueprint
from flask_restplus import Api
from app.core.views.system.auth_view import auth_dto_api
from app.core.views.system.user_view import user_dto_api

blueprint = Blueprint("api", __name__)
authorizations = {
    'oauth2': {
        'type': 'oauth2',
        'flow': 'password',
        'tokenUrl': 'http://127.0.0.1:8801/auth/token',
    }
}

api = Api(
    blueprint,
    title="Flask MSF",
    version="1.0",
    description="Flask Micro Services Framework",
    security=['apikey', {'oauth2': 'read'}], authorizations=authorizations
)

# Add Name Space
api.add_namespace(auth_dto_api)
api.add_namespace(user_dto_api, path="/user")
# api.add_namespace(test_dto_api, path='/test')
