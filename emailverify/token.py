import datetime
from run import *
import jwt

def generate_confirmation_token(email):
    # serializer = URLSafeSerializer(app.config['SECRET_KEY'])
    # return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])
    token = jwt.encode({'email': email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)}, app.config['SECRET_KEY'])
    return token


def confirm_token(token):
    data = jwt.decode(token, app.config['SECRET_KEY'])
    # current_user = users.query.filter_by(id=data['email']).first()
    current_user = data['email']
    return current_user
    # serializer = URLSafeSerializer(app.config['SECRET_KEY'])
    # try:
    #     email = serializer.loads(
    #         token,
    #         salt=app.config['SECURITY_PASSWORD_SALT'],
    #         max_age=expiration
    #     )
    # except:
    #     return False
    # return email