import re
import datetime

from flask import  request, jsonify, make_response, url_for, Blueprint
from werkzeug.security import check_password_hash,generate_password_hash
import jwt

from run import app,db
from common.decorator import token_required
from models.models import users
from emailverify.token import generate_confirmation_token,confirm_token
from emailverify.emailverify import send_email

user = Blueprint('user',__name__)


# # @user.before_request()
# def importrun():
#     from run import app, db
@user.route('/signup',methods=['POST'])
def signup():
    data =request.get_json()
    if not re.match(r"[^@]+@[^@]+\.[^@]+", data['email']):
        return jsonify({'message':'provide correct email '})
    user = users.query.filter_by(email=data['email']).first()
    if not user:
        hash_password = generate_password_hash(data['password'])
        new_user =users(email=data['email'],password=hash_password,confirmed=0)
        db.session.add(new_user)
        db.session.commit()


        token = generate_confirmation_token(new_user.email)

        # token1=str(token)
        # try:
        confirm_url = url_for('user.confirm_email', token=token, _external=True)
        # except Exception as e:
        # return jsonify({'message':'no'})
        # html = render_template('', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(new_user.email, subject,confirm_url)

        # return jsonify({'message':'new user is added'})
        return jsonify({'message': 'A confirmation email has been sent via email'})
    return jsonify({'message':'Email already registered'})


#decorator for change password
@user.route('/changePassword',methods=['PUT'])
@token_required
def changePassword(current_user):
    if not current_user:
        return jsonify({'message':'please login first to perform this operation'})
    data=request.get_json()
    if data['password'] !='':
        hashed_pass=generate_password_hash(data['password'])
        current_user.password=hashed_pass
        db.session.commit()
        return jsonify({'message':'password changed successfully'})
    return jsonify({'message':'password field is required'})


@user.route('/login')
def login():
    auth_data=request.authorization

    if not auth_data or not auth_data.username or not auth_data.password:
        return make_response('incorect login detail1',401,{'WWW-Authenticate':'Basic realm="Login required"'})
    user =users.query.filter_by(email=auth_data.username).first()
    if not user:
        return make_response('incorect email',401,{'WWW-Authenticate':'Basic realm="Login required"'})
     
    if check_password_hash(user.password,auth_data.password):
        if user.confirmed:
            token = jwt.encode({'id':user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)}, app.config['SECRET_KEY'])
            return jsonify({'token':token.decode('UTF-8')})
        else:
            return jsonify({'message':'please confirm your email before login'})
    return make_response('incorect login detail',401,{'WWW-Authenticate':'Basic realm="Login required"'})


@user.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
        # return jsonify({'message1': email})
    except:
        return jsonify({'message':'The confirmation link is invalid or has expired'})
    user = users.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        return  jsonify({'message':'Account already confirmed. Please login.'})
    else:
        user.confirmed = 1

        # user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'Thanks for confirming the email !you can login now'})

    # return redirect(url_for('main.home'))