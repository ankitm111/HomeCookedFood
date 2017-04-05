import os
from flask import Flask, jsonify, abort, request, g
from datetime import datetime
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

#from models import Users, Tiffins, Comments, Ratings
# TODO: Fix CICRULAR IMPORTS
import models


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@auth.verify_password
def verify_password(email_id_or_token, password):
    # first try to authenticate by token
    user = models.Users.verify_auth_token(email_id_or_token)
    if not user:
        # try to authenticate with user_id/password
        user = models.Users.query.filter_by(email_id=email_id_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route('/homecookedfood/token', methods=['GET'])
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')}) 


@app.route('/homecookedfood/adduser', methods=['POST'])
def adduser():
    content = request.json
    if (not content or not 'name' in content or not 'email_id' in content
        or not 'password' in content or not 'phone' in content or
        not 'zipcode' in content):
        abort(400)

    user = models.Users.query.filter_by(email_id=content['email_id']).first()
    if user is not None:
        # existing user
        abort(400)

    new_user = models.Users(content['name'], content['email_id'], content.get('phone'), content.get('zipcode'))
    new_user.hash_password(content['password'])

    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id' : new_user.user_id}), 201


@app.route('/homecookedfood/addtiffin', methods=['POST'])
@auth.login_required
def addtiffin():
    content = request.json
    user_id = g.user.user_id

    if (not content or not 'tiffin_details' in content or not price_per_tiffin in content):
        abort(400)

    tiffin = models.Tiffins(user_id, content['tiffin_details'], content['price_per_tiffin'], max_tiffins = content.get('max_tiffins', 0))

    g.user.make_provider() 

    db.session.add(tiffin)
    db.session.commit()
    return jsonify({}), 201


@app.route('/homecookedfood/getprovidersbyzipcode', methods=['GET'])
@auth.login_required
def getprovidersbyzipcode():
    content = request.json
    
    if (not content or not 'zipcode' in content):
        abort(400)

    users = models.Users.query.filter_by(zipcode=content['zipcode'], is_provider=True)
    return jsonify({'list_of_providers': users}), 201


@app.route('/homecookedfood/gettiffinsbyprovider', methods=['GET'])
@auth.login_required
def gettiffinsbyprovider():
    content = request.json
    
    if (not content or not 'provider_id' in content):
        abort(400)

    user = models.Users.query.filter_by(user_id=content['provider_id']).first()
    return jsonify({'tiffins_by_provider': user.tiffins}), 201

    
@app.route('/homecookedfood/gettiffinsbyzipcode', methods=['GET'])
@auth.login_required
def gettiffinsbyzipcode():
    content = request.json
    
    if (not content or not 'zipcode' in content):
        abort(400)

    tiffins = []
    users = models.Users.query.filter_by(zipcode=content['zipcode'])
    for user in users:
        list_of_tiffins_user = user.tiffins
        for tiffin in list_of_tiffins_user:
            tiffins.append(tiffin)

    return jsonify({'list_of_tiffins': tiffins}), 201


@app.route('/homecookedfood/givecommenttoprovider', methods=['POST'])
@auth.login_required
def givecommenttoprovider():
    content = request.json
    
    if (not content or not 'provider_id' in content):
        abort(400)

    if (not 'comment' in content and not 'rating' in content):
        abort(400)

    cmt = content.get('comment', '')
    rating = content.get('rating', 0)

    comment = models.Comments(content['provider_id'], g.user.user_id,
                              cmt, rating, datetime.now())

    user = models.Users.query.filter_by(user_id=content['provider_id']).first()
    user.update_rating(rating) 
      
    db.session.add(comment)
    db.session.commit()


if __name__ == '__main__':
    app.run()
