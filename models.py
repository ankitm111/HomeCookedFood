from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(db.String(40))
    password = db.Column(db.String(80))
    phone_number = db.Column(db.String(11))
    zipcode = db.Column(db.String(10))
    dishes = db.relationship('FoodServed', backref='users',
                             lazy='dynamic')

    def __init__(self, email_id, password, phone_number, zipcode):
        self.email_id = email_id
        self.password = password
        self.phone_number = phone_number
        self.zipcode = zipcode

    def __repr__(self):
        return '<id {}>'.format(self.id)


#FoodServed:  (Drop all the rows with stale Date each day)
class FoodServed(db.Model):
    __tablename__ = 'foodserved'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    dishes = db.Column(JSON)
    datetime = db.Column(db.DateTime)
   
    def __init__(self, user_id, dishes, datetime):
        self.user_id = user_id
        self.dishes = dishes
        self.datetime = datetime

    def __repr__(self):
        return '<id {}>'.format(self.id)
 

class Comments(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    commenter_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comment = db.Column(db.String(100))
    rating = db.Column(db.Float)
    datetime = db.Column(db.DateTime)

    def __init__(self, user_id, commenter_id, comment='', rating=5):
        self.user_id = user_id
        self.commenter_id = commenter_id
        self.comment = comment
        self.datetime = datetime.now()

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Ratings(db.Model):
    __tablename__ = 'ratings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    rating = db.Column(db.Float)
    num_ratings = db.Column(db.Integer)

    def __init__(self, user_id, rating, num_ratings):
        self.user_id = user_id
        self.rating = rating
        self.num_ratings = num_ratings

    def __repr__(self):
        return '<id {}>'.format(self.id)
