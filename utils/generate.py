from flask import url_for, request,render_template, flash,  redirect, session, Blueprint
import uuid
#from utils import urls, app
import re
from datetime import datetime
from flask_login import login_required, current_user
from .models import Url
from . import db, app


generate = Blueprint("generate", __name__)

regex = "(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,}|[a-zA-Z0-9]+\.[^\s]{2,})"


@generate.route("/generate_hash", methods=["POST"])
@login_required
def generate_hash():
	error = None
	try:
		result = re.match(regex, request.form.get("url"))
		if result is None:
			flash(app.config.get("ERR_FORMAT"))
			return redirect(url_for("main.profile"))
		if "http" not in request.form.get("url"):	
			session["url"] = "http://" + request.form.get("url")
		else:
			session["url"] = request.form.get("url")
		
		temp = str(uuid.uuid4())
		session["hash"]=temp[:8]

		new_url = Url(user_id=current_user.id, short_hash=session["hash"], url=session["url"], time_created=datetime.now())
		db.session.add(new_url)
		db.session.commit()		
		
		return redirect(url_for("main.success"))

	except:
		flash(app.config.get("ERR"))
		return redirect(url_for("main.profile"))


@generate.route("/custom_hash", methods=["POST"])
@login_required
def custom_hash():
	error = None
	try:
		result = re.match(regex, request.form.get("custom-url"))
		if result is None:
			flash(app.config.get("ERR_FORMAT"))
			return redirect(url_for("main.profile"))

		if "http" not in request.form.get("custom-url"):	
			session["url"] = "http://" + request.form.get("custom-url")
		else:
			session["url"] = request.form.get("custom-url")
		
		session["hash"]=request.form.get("hash")
		
		#check if hash already exists
		
		check = Url.query.filter_by(short_hash=session["hash"]).first()
		
		if check:
			flash(app.config.get("ERR_HASH"))
			return redirect(url_for("main.profile"))

		new_url = Url(user_id=current_user.id, short_hash=session["hash"], url=session["url"], time_created=datetime.now())		

		db.session.add(new_url)
		db.session.commit()		
		
		return redirect(url_for("main.success"))

	except:
		flash(app.config.get("ERR"))
		return redirect(url_for("main.profile"))


@generate.route("/urls")
@login_required
def urls():
	user_id = current_user.id
	urls = Url.query.filter_by(user_id=user_id)
	list_urls = []
	for i in urls:
		list_urls.append(i)
	if len(list_urls) > 0:		
		return render_template("urls.html", urls=list_urls)
	return render_template("urls.html")


@generate.route("/delete/<uid>")
@login_required
def delete(uid):
	user_id = current_user.id
	try:
		Url.query.filter(Url.user_id == user_id, Url.id == uid).delete()
		db.session.commit()
	except:
		flash(app.config.get("ERR_DELETE"))
	return redirect(url_for("generate.urls"))
	

@generate.route('/convert')
@login_required
def convert():
	return render_template("convert.html")


@generate.route("/convert", methods=["POST"])
@login_required
def convert_post():
	short_url = request.form.get("short_url")
	switch = app.config.get("SWITCH")
	#app.logger.info(switch)
	if switch:
		urls = Url.query.filter(Url.user_id==current_user.id, Url.short_hash==short_url).first()
		try:
			return render_template("success.html", original_url=urls.url, custom_url=short_url)
		except:
			return render_template("urls.html")
	else:
		urls = Url.query.filter_by(short_hash=short_url).first()
		try:
			return render_template("success.html", original_url=urls.url, custom_url=short_url)
		except:
			return render_template("urls.html")
