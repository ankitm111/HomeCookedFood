import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/homecookedfood'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Users, Tiffins, Comments, Ratings


@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run()
