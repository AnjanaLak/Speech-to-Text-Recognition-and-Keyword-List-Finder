from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from audioClassification import main

app = Flask(__name__)  # is a special variable in python that is just the name of the module
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///saak.db'  # '///' means the relative path from current directory
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

from audioClassification import routes

# this part shout include inside a route function


