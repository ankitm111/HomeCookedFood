import random
import string
import datetime
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
    rating = db.Column(db.Float)
    num_ratings = db.Column(db.Integer)
    is_provider = db.Column(db.Boolean)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    meals = db.relationship('Meal', backref='provider',
                            lazy='dynamic')
    '''
    TODO: See how to add comments as relationship here
    comments = db.relationship('Comments', backref='user',
                               lazy='dynamic')
    '''

    def __init__(self, username, name, email_id, phone_number,
                 longitude, latitude):
        self.username = username
        self.name = name
        self.email_id = email_id
        self.phone_number = phone_number
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

    def generate_auth_token(self, expiration=60000):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'user_id': self.user_id})

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
            return None  # valid token, but expired
        except BadSignature as e:
            return None  # invalid token
        user = Users.query.filter_by(user_id=data['user_id']).first()
        return user


# Meal:  (Drop all the rows with stale Date each day)
class Meal(db.Model):
    __tablename__ = 'meal'

    meal_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    provider_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    price = db.Column(db.Float)
    #max_count = db.Column(db.Integer)
    date_time_pickup = db.Column(db.DateTime)
    date_time_last_order = db.Column(db.DateTime)
    items = db.relationship('MealItems', lazy='dynamic')
    #tags = db.relationship('MealTags', lazy='dynamic')

    def __init__(self, name, provider_id, price,
                 date_time_pickup, date_time_last_order):
        self.provider_id = provider_id
        self.name = name
        self.price = price
        #self.max_count = max_count
        self.date_time_pickup = date_time_pickup
        self.date_time_last_order = date_time_last_order

    def __repr__(self):
        return '<name {}>'.format(self.name)

class MealItems(db.Model):
    __tablename__ = 'mealitems'
    item_name = db.Column(db.String(128), primary_key=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.meal_id'),
                        primary_key=True)
    #item_count = db.Column(db.Integer)

    def __init__(self, item_name, meal_id):
        self.item_name = item_name
        self.meal_id = meal_id
        #self.item_count = item_count

    def __repr__(self):
        return '<item_name {}>'.format(self.item_name)


# For now, commenting the Tags
"""
class MealTags(db.Model):
    __tablename__ = 'mealtags'
    # XXX Maybe we need a separate tag table and this should be tag id.
    tag_name = db.Column(db.String(128), primary_key=True)
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.meal_id'),
                        primary_key=True)

    def __init__(self, tag_name, meal_id):
        self.tag_name = tag_name
        self.meal_id = meal_id

    def __repr__(self):
        return '<tag_name {}>'.format(self.tag_name)
"""

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
