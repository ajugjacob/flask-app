from flask import Blueprint, redirect, render_template, session
from . import db
from flask_login import login_required, current_user
from .models import Url

main = Blueprint("main", __name__)

@main.after_request
def add_header(response):
	response.headers['Cache-Control'] =  'no-store, no-cache, must-revalidate, post-check=0, pre-check=0'
	return response


@main.route('/')
def index():
	return render_template("index.html")


@main.route('/profile')
@login_required
def profile():
	return render_template("profile.html")

@main.route("/<url_hash>")
def custom_redirect(url_hash):
	result = Url.query.filter_by(short_hash=url_hash).first()
	if result:
		return redirect(str(result.url), code=301)
	return render_template("urls.html")


@main.route("/success")
@login_required
def success():
	return render_template("success.html", original_url=session["url"], custom_url="3.110.132.199/"+session["hash"])
