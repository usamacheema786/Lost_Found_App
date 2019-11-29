import jwt

from flask import request,jsonify
from functools import wraps

from run import app


def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token =None
        if 'access-token' in request.headers:
            token = request.headers['access-token']
        if not token:
            return jsonify({'message':'Token is miising'})
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = users.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message':'Invalid token'}),401

        return f(current_user,*args,**kwargs)
    return decorated
