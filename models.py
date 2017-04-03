from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON


class Users(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(db.String(40))
    password = db.Column(db.String(80))
    phone_number = db.Column(db.String(11))
    zipcode = db.Column(db.String(10))
    dishes = db.relationship('Tiffins', backref='users',
                             lazy='dynamic')

    def __init__(self, email_id, password, phone_number, zipcode):
        self.email_id = email_id
        self.password = password
        self.phone_number = phone_number
        self.zipcode = zipcode

    def __repr__(self):
        return '<id {}>'.format(self.user_id)


#Tiffins:  (Drop all the rows with stale Date each day)
class Tiffins(db.Model):
    __tablename__ = 'tiffins'

    tiffin_id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    tiffin_details = db.Column(JSON)
    date_time = db.Column(db.DateTime)
    max_tiffins = db.Column(db.Integer)
   
    def __init__(self, provider_id, tiffin_details, datetime=datetime.now(), max_tiffins=0):
        self.provider_id = provider_id
        self.tiffin_details = tiffin_details
        self.date_time = date_time
        self.max_tiffins = max_tiffins

    def __repr__(self):
        return '<id {}>'.format(self.tiffin_id)
 

class Comments(db.Model):
    __tablename__ = 'comments'

    comment_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    commenter_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    comment = db.Column(db.String(100))
    rating = db.Column(db.Float)
    datetime = db.Column(db.DateTime)

    def __init__(self, user_id, commenter_id, comment='', rating=5):
        self.user_id = user_id
        self.commenter_id = commenter_id
        self.comment = comment
        self.datetime = datetime.now()

    def __repr__(self):
        return '<id {}>'.format(self.comment_id)


class Ratings(db.Model):
    __tablename__ = 'ratings'

    rating_id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    rating = db.Column(db.Float)
    num_ratings = db.Column(db.Integer)

    def __init__(self, provider_id, rating, num_ratings):
        self.provider_id = provider_id
        self.rating = rating
        self.num_ratings = num_ratings
