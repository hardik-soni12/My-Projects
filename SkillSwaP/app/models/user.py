from app import db, bcrypt, login_manager
from flask_login import UserMixin

# Flask-Login will use this to load the logged-in user from the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), nullable = False, unique = True)
    email = db.Column(db.String(120), nullable = False, unique = True)
    password = db.Column(db.String(200), nullable = False)

def set_password(self,raw_password):
    self.password = bcrypt.generate_password_hash(raw_password).decode('utf-8')

def check_password(self, attempted_password):
    return bcrypt.check_password_hash(self.password, attempted_password)

def __repr__(self):
    return f'<User {self.username}>'