from flask import Blueprint, request
from flask_restful import Resource, marshal_with, fields, abort, Api


auth_bp = Blueprint("auth_bp", __name__, url_prefix='/auth')
auth_api = Api(auth_bp)

users_db = {
    'hardik123@gmail.com': 'password123'
}

class Register(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            abort(400, {'error': 'email and password required'})
        if email in users_db:
            abort(400, {'error': 'user already exists'})
        users_db[email] = password
        return {'msg':'User registered'}, 201
    
class Login(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        if email in users_db and users_db[email] == password:
            return {'token':'fake-jwt-token'}, 201
        return {'error': 'Invalid credentials'}, 401
    
auth_api.add_resource(Register, '/register')
auth_api.add_resource(Login, '/login')