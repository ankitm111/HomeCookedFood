import os
import random, string
from app import db, app
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON


def randomiamgename(length=20):
   return ''.join(random.choice(string.lowercase) for i in range(length))


class Users(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    name = db.Column(db.String(40))
    email_id = db.Column(db.String(40), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    phone_number = db.Column(db.String(11))
    zipcode = db.Column(db.String(10))
    rating = db.Column(db.Float)
    num_ratings = db.Column(db.Integer)
    is_provider = db.Column(db.Boolean)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    meals = db.relationship('Meal', backref='provider',
                            lazy='dynamic')
    # TODO: See how to add comments as relationship here
    #comments = db.relationship('Comments', backref='user',
    #                           lazy='dynamic')


    def __init__(self, username, name, email_id, phone_number, zipcode,
                 longitude, latitude):
        self.username = username
        self.name = name
        self.email_id = email_id
        self.phone_number = phone_number
        self.zipcode = zipcode
        self.rating = 0.0
        self.num_ratings = 0
        self.is_provider = False
        self.longitude = longitude
        self.latitude = latitude

    def __repr__(self):
        return '<id {}>'.format(self.user_id)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration = 60000):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'user_id': self.user_id })

    def make_provider(self):
        self.is_provider = True

    def update_rating(self, rating):
        rat = float(self.rating * self.num_ratings)
        rat = rat + rating
        self.num_ratings = self.num_ratings + 1
        self.rating = float(rat / self.num_ratings)

    def __json__(self):
        return dict(username=self.username,
                    name=self.name,
                    email_id=self.email_id,
                    phone_number=self.phone_number,
                    zipcode=self.zipcode,
                    rating=self.rating,
                    num_ratings=self.num_ratings,
                    longitude=self.longitude,
                    latitude=self.latitude)

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = Users.query.filter_by(user_id=data['user_id']).first()
        return user


#Meal:  (Drop all the rows with stale Date each day)
class Meal(db.Model):
    __tablename__ = 'meal'

    meal_id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    meal_details = db.Column(JSON)
    price_per_meal = db.Column(db.Integer)
    max_meals = db.Column(db.Integer)
    tags = db.Column(db.String(50))
    date_time = db.Column(db.DateTime)
   
    def __init__(self, provider_id, meal_details,
                 price_per_meal, max_meals=0, tags='',
                 date_time=datetime.now()):
        self.provider_id = provider_id
        self.meal_details = meal_details
        self.price_per_meal = price_per_meal
        self.max_meals = max_meals
        self.tags = tags
        self.date_time = date_time

    def __repr__(self):
        return '<id {}>'.format(self.meal_id)
 

class Comments(db.Model):
    __tablename__ = 'comments'

    comment_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    commenter_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    comment = db.Column(db.String(100))
    rating = db.Column(db.Integer)
    date_time = db.Column(db.DateTime)

    def __init__(self, user_id, commenter_id, comment='', rating=0):
        self.user_id = user_id
        self.commenter_id = commenter_id
        self.comment = comment
        self.rating = rating
        self.date_time = datetime.now()

    def __repr__(self):
        return '<id {}>'.format(self.comment_id)
