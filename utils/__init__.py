from flask import Flask
from flask_session import Session
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import logging

db = SQLAlchemy()

logging.basicConfig(filename='demo.log', level=logging.DEBUG)
	
app = Flask(__name__)
	
app.config.from_pyfile(os.path.join(".", "config/app.conf"), silent=False)

app.config['SECRET_KEY'] = app.config.get("SECRET_KEY")

app.config['SQLALCHEMY_DATABASE_URI'] = app.config.get("DB_URI")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
	
Session(app)

db.init_app(app)
	
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from .models import User

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
    return response


# auth routes blueprints
from .auth import auth as auth_blueprints
app.register_blueprint(auth_blueprints)

# not auth routes blueprints
from .main import main as main_blueprints
app.register_blueprint(main_blueprints)

# hashing routes blueprints
from .generate import generate as generate_blueprints
app.register_blueprint(generate_blueprints)


#if __name__ == "__main__":
#	app.run()
