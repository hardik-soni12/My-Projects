from flask import Flask
from flask_jwt_extended import JWTManager


jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'my-secret-key'
    app.config['JWT_SECRET_KEY'] = 'my-jwt-secret-key'

    jwt.init_app(app)

    from app.auth.routes import auth_bp
    from app.users.routes import users_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)

    return app