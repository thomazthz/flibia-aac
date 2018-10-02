import hashlib
from functools import wraps

from flask import current_app, redirect, url_for
from flask_login import current_user
from itsdangerous import URLSafeTimedSerializer


def generate_hash_password(password):
    return hashlib.sha1(password.encode('ascii')).hexdigest()


def check_password(pwhash, password):
    # Very weak =/ (compatibility with forgottenserver password)
    return pwhash == generate_hash_password(password)


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['TOKEN_SALT'])


def confirm_email_confirmation_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=current_app.config['TOKEN_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email


def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.creation:
            return redirect(url_for('account.unconfirmed'))
        return func(*args, **kwargs)

    return decorated_function
