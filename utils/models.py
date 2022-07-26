from . import db
from sqlalchemy.sql import func
from flask_login import UserMixin

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
	email = db.Column(db.String(100), unique=True)
	password = db.Column(db.String(100))
	name = db.Column(db.String(1000))

class Url(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer)
	short_hash = db.Column(db.String(20), unique=True)
	url = db.Column(db.String(100))
	time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
