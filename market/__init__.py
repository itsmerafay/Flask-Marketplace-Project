# Here we have defined the default configuration for our application
# We have to initialize the instance of the decrypt library for passowrd hash
# Getters and setters help you maintain data encapsulation, abstraction, and validation, promoting cleaner and more maintainable code.

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__, static_url_path='/static')

# Configuration for SQLAlchemy, Bcrypt, and LoginManager
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = '008035dca5ea8092e61a8351'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"
from market import routes