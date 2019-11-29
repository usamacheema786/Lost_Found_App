from run import db
# Databse Models
class users(db.Model):
    __tablename__='users'

    id = db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(255))
    password=db.Column(db.String(255))
    confirmed=db.Column(db.Integer)
    # item=db.relationship('items',backref='users',lazy='dynamic')

class items(db.Model):
    __tablename__='items'
    
    id = db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(255))
    description=db.Column(db.String(10000))
    category=db.Column(db.String(255))
    location=db.Column(db.String(255))
    date=db.Column(db.String(255))
    user_id=db.Column(db.Integer)
    image_path=db.Column(db.String(255))
