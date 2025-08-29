from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from config import Config


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    jwt = JWTManager(app)
    api = Api(app)


    from app.auth.routes import auth_bp
    from app.users.routes import users_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)

    return app