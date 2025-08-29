from flask import Blueprint
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, get_jwt_identity



users_bp = Blueprint('users_bp', __name__, url_prefix='/user')
user_api = Api(users_bp)

class Profile(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        return {"user":f"Hello, {current_user}"}, 200
    
user_api.add_resource(Profile, '/profile')