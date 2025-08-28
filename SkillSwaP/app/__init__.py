from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'mysecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'orgskillswap@gmail.com'
    app.config['MAIL_PASSWORD'] = 'iinb fzqd ibsf jabs'  # App password
    app.config['MAIL_DEFAULT_SENDER'] = 'orgskillswap@gmail.com'

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.skills import skills_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(skills_bp)

    return app