from flask import Blueprint, request
from flask_restful import Resource, Api



users_bp = Blueprint('users_bp', __name__, url_prefix='/user')
user_api = Api(users_bp)

class Users(Resource):
    def get(self):
        return {'users':["Alice", "Bob"]}, 200
    
user_api.add_resource(Users, '/users')