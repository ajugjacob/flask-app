from flask import Blueprint, render_template, flash, url_for, redirect, request
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db, app
from flask_login import login_user, login_required, logout_user

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
	return render_template("login.html")


@auth.route('/login', methods=['POST'])
def login_post():
	email = request.form.get("email")
	password = request.form.get("password")
	
	remember = True if request.form.get("remember") else False

	user = User.query.filter_by(email=email).first()

	if not user or not check_password_hash(user.password, password):
		flash(app.config.get("ERR_AUTH"))
		return redirect(url_for("auth.login"))
	login_user(user, remember=remember)
	return redirect(url_for("main.profile"))



@auth.route('/signup')
def signup():
	return render_template("signup.html")


@auth.route('/signup', methods=["POST"])
def signup_post():
	email = request.form.get("email")
	name = request.form.get("name")
	password = request.form.get("password")

	user = User.query.filter_by(email=email).first()

	if user:
		flash(app.config.get("ERR_EMAIL"))
		return redirect(url_for("auth.login"))

	new_user = User(email=email, name=name, password=generate_password_hash(password, method="sha256"))

	db.session.add(new_user)
	db.session.commit()

	return redirect(url_for("auth.login"))


@auth.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for("main.index"))
