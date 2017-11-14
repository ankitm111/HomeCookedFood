import os
import json
import logging
from logging.handlers import RotatingFileHandler

from datetime import datetime
from functools import wraps
from collections import namedtuple

from flask import Flask, jsonify, abort, request, g, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_migrate import Migrate
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/homecookedfood'
app.config['SECRET_KEY'] = 'AnkitHarshOnkar'

# allow cross domain requests to succeed
CORS(app, supports_credentials=True)


db = SQLAlchemy(app)
migrate = Migrate(app, db)
auth = HTTPBasicAuth()

# from models import Users, Meal, Comments, Ratings
# TODO: Fix CICRULAR IMPORTS, COMMON FLASK PROBLEM
import models


def validate_json(*variable_args):
    """
    Decorator used to do basic validation of the incoming request. It simply
    checks if the passed arguments are present in request.json. This can be
    used to avoid repetitive if checks.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not request.json:
                abort(400)
            for va in variable_args:
                if va not in request.json:
                    abort(400)
            return func(*args, **kwargs)
        return wrapper
    return decorator


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    with open("/tmp/b", "a") as f:
        f.write("Trying to auth (%s , %s)\n " % (username_or_token, password))
    user = models.Users.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with user_id/password
        user = models.Users.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route('/hcf/token', methods=['GET'])
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii'), 'name': g.user.name}), 200


@app.route('/hcf/users/<string:username>', methods=['POST'])
@validate_json('name', 'email_id', 'password', 'phone')
def adduser(username):
    content = request.json
    user = models.Users.query.filter(
        (models.Users.username == username) |
        (models.Users.email_id == content['email_id'])).first()
    if user is not None:
        # existing user
        abort(400)

    new_user = models.Users(username, content.get('name'),
                            content.get('email_id'), content.get('phone'),
                            content.get('longitude'), content.get('latitude'))
    new_user.hash_password(content.get('password'))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id': new_user.user_id}), 201


@app.route('/hcf/users/getcurrentuser', methods=['GET'])
@auth.login_required
def getcurrentuser():
    return jsonify({'user': g.user.__json__()}), 201


@app.route('/hcf/users/provider/meals/<string:mealname>', methods=['POST'])
@auth.login_required
#@validate_json('price', 'tagnames', 'max_count', 'meal_items')
#@validate_json('price', 'tagnames', 'meal_items')
def createmeal(mealname):
    content = request.json
    user_id = g.user.user_id
    date_time = content.get('date_time', datetime.now().strftime('%Y%m%d-%H%M%S'))
    meal = models.Meal(mealname, user_id, content['price'],
                       max_count=0,
                       date_time=date_time)
    db.session.add(meal)
    db.session.flush()

    for item_name, item_count in content['meal_items'].iteritems():
        db.session.add(models.MealItems(item_name, meal.meal_id, item_count))

    #for tag_name in content['tagnames']:
    db.session.add(models.MealTags(content['tagnames'], meal.meal_id))

    db.session.commit()
    print("Meal added successfully")
    return jsonify({}), 201


@app.route('/hcf/users/provider/meals/<string:mealname>', methods=['GET'])
@auth.login_required
def getmeal(mealname):
    user_id = g.user.user_id
    mealinfo_lst = models.Meal.query.filter_by(provider_id=user_id,
                                               name=mealname)
    if mealinfo_lst.count() == 0:
        abort(404)

    mealinfo = mealinfo_lst[0]
    result = {"price": mealinfo.price, "max_count": mealinfo.max_count,
              "date_time": mealinfo.date_time.strftime('%Y%m%d-%H%M%S')}
    result["tagnames"] = [e.tag_name for e in mealinfo.tags]
    result["meal_items"] = [[e.item_name, e.item_count] for e in mealinfo.items]
    return jsonify(result), 201
    

@app.route('/hcf/users/provider/meals', methods=['GET'])
@auth.login_required
def listmeals():
    user_id = g.user.user_id
    mealinfo_lst = models.Meal.query.filter_by(provider_id=user_id)

    result = []
    for mealinfo in mealinfo_lst:
        result.append(mealinfo.name)
    return jsonify(result), 201


@app.route('/hcf/getprovidersbycoordinates', methods=['GET'])
@auth.login_required
@validate_json('longitude', 'latitude')
def getprovidersbycoordinates():
    """
    This logic is shamelessly copied from the following URL -
    http://www.plumislandmedia.net/mysql/haversine-mysql-nearest-loc/
    """
    content = request.json
    longitude = content['longitude']
    latitude = content['latitude']
    radius = '50.0'
    distance_unit = '69.0'
    limit = '15'

    sql = '''
    SELECT u.name, u.phone_number, u.rating, u.num_ratings, u.email_id,
           p.distance_unit
               * DEGREES(ACOS(COS(RADIANS(p.latpoint))
               * COS(RADIANS(u.latitude))
               * COS(RADIANS(p.longpoint) - RADIANS(u.longitude))
               + SIN(RADIANS(p.latpoint))
               * SIN(RADIANS(u.latitude)))) AS distance_in_miles
    FROM users as u
    JOIN (SELECT %s AS latpoint, %s AS longpoint,
          %s AS radius, %s AS distance_unit) AS p ON 1=1
    WHERE u.is_provider = 'true'
    AND u.latitude
        BETWEEN p.latpoint - (p.radius / p.distance_unit)
            AND p.latpoint + (p.radius / p.distance_unit)
        AND u.longitude BETWEEN
        p.longpoint - (p.radius / (p.distance_unit * COS(RADIANS(p.latpoint))))
        AND p.longpoint +
        (p.radius / (p.distance_unit * COS(RADIANS(p.latpoint))))
    ORDER BY distance_in_miles
    LIMIT %s
    ''' % (latitude, longitude, radius, distance_unit, limit)

    result = db.engine.execute(text(sql))
    record = namedtuple('record', result.keys())
    records = [record(*r) for r in result.fetchall()]
    return jsonify({'list_of_providers': records}), 201


@app.route('/hcf/getmealsbyprovider', methods=['GET'])
@auth.login_required
@validate_json('provider_id')
def getmealsbyprovider():
    content = request.json
    user = models.Users.query.filter_by(user_id=content['provider_id']).first()
    return jsonify({'meals_by_provider': user.meals}), 201


@app.route('/hcf/givecommenttoprovider', methods=['POST'])
@auth.login_required
@validate_json('provider_id', 'comment', 'rating')
def givecommenttoprovider():
    content = request.json
    rating = content.get('rating', 0)
    comment = models.Comments(content['provider_id'], g.user.user_id,
                              content.get('comment', ''),
                              int(content.get('rating', 0)), datetime.now())
    user = models.Users.query.filter_by(user_id=content['provider_id']).first()
    user.update_rating(rating)
    db.session.add(comment)
    db.session.commit()


if __name__ == '__main__':
    app.run(threaded=True)
