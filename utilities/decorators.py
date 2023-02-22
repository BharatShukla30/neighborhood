from functools import wraps
from flask import request, current_app
import jwt


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return {'error': 'Authorization header is missing'}, 401
        token = auth_header.split(" ")[1]
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return {'error': 'Token has expired'}, 401
        except jwt.InvalidTokenError:
            return {'error': 'Invalid token'}, 401
        return f(user_id, *args, **kwargs)
    return decorated_function
