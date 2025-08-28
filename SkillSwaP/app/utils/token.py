from flask import current_app
from itsdangerous import URLSafeTimedSerializer

def generate_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='email-verify')

def verify_token(token, expiration=1800):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email= serializer.loads(token, salt='email-verify', max_age=expiration)
    except Exception:
        return None
    return email