import os
import json
from datetime import datetime
from functools import wraps

from flask import Flask, jsonify, abort, request, g, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/homecookedfood'
app.config['SECRET_KEY'] = 'AnkitHarshOnkar'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
auth = HTTPBasicAuth()

#from models import Users, Meal, Comments, Ratings
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
    return jsonify({'token': token.decode('ascii')}) 


@app.route('/hcf/users/<string:username>', methods=['POST'])
@validate_json('name', 'email_id', 'password', 'phone', 'zipcode')
def adduser(username):
    content = request.json
    user = models.Users.query.filter((models.Users.username == username) |
        (models.Users.email_id == content['email_id'])).first()
    if user is not None:
        # existing user
        abort(400)

    new_user = models.Users(username, content['name'],
                            content['email_id'], content.get('phone'),
                            content.get('zipcode'))
    new_user.hash_password(content['password'])

    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id' : new_user.user_id}), 201


@app.route('/hcf/users/getcurrentuser', methods=['GET'])
@auth.login_required
def getcurrentuser():
    return jsonify({'user' : g.user.__json__()}), 201


@app.route('/hcf/addmeal', methods=['POST'])
@auth.login_required
@validate_json('meal_details', 'price_per_meal')
def addmeal():
    content = request.json
    user_id = g.user.user_id

    meal = models.Meal(user_id, content['meal_details'],
                       content['price_per_meal'],
                       max_meals = content.get('max_meals', 0))

    g.user.make_provider() 

    db.session.add(meal)
    db.session.commit()
    return jsonify({}), 201


@app.route('/hcf/getprovidersbyzipcode', methods=['GET'])
@auth.login_required
@validate_json('zipcode')
def getprovidersbyzipcode():
    content = request.json
    users = models.Users.query.filter_by(zipcode=content['zipcode'],
                                         is_provider=True)
    return jsonify({'list_of_providers': users}), 201


@app.route('/hcf/getmealsbyprovider', methods=['GET'])
@auth.login_required
@validate_json('provider_id')
def getmealsbyprovider():
    content = request.json
    user = models.Users.query.filter_by(user_id=content['provider_id']).first()
    return jsonify({'meals_by_provider': user.meals}), 201

    
@app.route('/hcf/getmealsbyzipcode', methods=['GET'])
@auth.login_required
@validate_json('zipcode')
def getmealsbyzipcode():
    content = request.json
    meals = []
    users = models.Users.query.filter_by(zipcode=content['zipcode'])
    for user in users:
        list_of_meals_user = user.meals
        for meal in list_of_meals_user:
            meals.append(meal)

    return jsonify({'list_of_meals': meals}), 201


@app.route('/hcf/givecommenttoprovider', methods=['POST'])
@auth.login_required
@validate_json('provider_id', 'comment', 'rating')
def givecommenttoprovider():
    content = request.json

    cmt = content.get('comment', '')
    rating = content.get('rating', 0)

    comment = models.Comments(content['provider_id'], g.user.user_id,
                              content.get('comment', ''),
                              int(content.get('rating', 0)), datetime.now())

    user = models.Users.query.filter_by(user_id=content['provider_id']).first()
    user.update_rating(rating) 
      
    db.session.add(comment)
    db.session.commit()


if __name__ == '__main__':
    app.run()
