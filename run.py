# from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask import Flask

app = Flask(__name__)




db = SQLAlchemy(app)

# from config import ProductionConfig
# app.config.from_object(ProductionConfig())


# from werkzeug.utils import import_string
# cfg = import_string('config.ProductionConfig')()
# app.config.from_object(cfg)
mail = Mail(app)

app.config['SECRET_KEY'] = 'secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://usama:root@mysql:3306/found_lost'
#
app.config['SECURITY_PASSWORD_SALT'] = 'my_precious_two'
# mail settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_SE_SSL'] = True

# gmail authentication
app.config['MAIL_USERNAME'] = 'abc745588@gmail.com'
app.config['MAIL_PASSWORD'] = 'muslim123'

# mail accounts
app.config['MAIL_DEFAULT_SENDER'] = 'abc745588@gmail.com'
# with app.app_context():
#     db.create_all()
# from user.api import *
# from item.api import *

if __name__ == "__main__":
    # from config import ProductionConfig
    #
    # app.config.from_object(ProductionConfig())
    from user.api import user
    app.register_blueprint(user)

    from item.api import item
    app.register_blueprint(item)
    app.run(host='0.0.0.0', debug=True)
