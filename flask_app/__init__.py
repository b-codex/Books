from datetime import timedelta
from flask_app.dbModels import *
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.debug=True
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = '8c99c41ad2fdd25e3ba8881e7f6fb887'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://wxgncdozyktlun:09e460eb130ae553eee73db6d86051c28cab55b6591075e58f635e45a57a9a0e@ec2-3-91-127-228.compute-1.amazonaws.com:5432/d8i4kufqlg4jnh"

app.permanent_session_lifetime = timedelta(days=7)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from flask_app import routes
# create_users_table("Users")
# create_comments_table("Comments")