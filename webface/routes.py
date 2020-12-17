######################################################################################
import string
import random
import functools
from . import app
from pony.orm import db_session
from .models import User, Shortener
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, request, redirect, url_for, session, flash
######################################################################################
def login_required(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        if "user" in session:
            return function(*args, **kwargs)
        else:
            return redirect(url_for("login", url=request.path))
    return wrapper
######################################################################################
@app.route("/", methods=["GET"])
@db_session
def index():
    shortcut = "".join([random.choice(string.ascii_letters) for i in range(7)])
    print(shortcut)
    if "user" in session:
        user = User.get(login=session["user"])
        for addr in user.addresses:
            print(addr.shortcut, addr.url)
    return render_template("base.html.j2")
######################################################################################
@app.route("/<string:shortcut>", methods=["GET"])
@db_session
def short_redirect(shortcut):
    shortener = Shortener.get(shortcut=shortcut)
    if shortener.user:
        print(shortener.user.login)
    return render_template("base.html.j2")
######################################################################################
@app.route("/adduser/", methods=["GET"])
@db_session
def adduser():
    return render_template("adduser.html.j2")
######################################################################################
@app.route("/adduser/", methods=["POST"])
@db_session
def adduser_post():
    login = request.form.get("login")
    passwd1 = request.form.get("passwd1")
    passwd2 = request.form.get("passwd2")
    user = User.get(login=login)
    if user:
        flash("Daný uživatel již existuje")
        print(user.login, user.password)
    elif len(passwd1) >= 6 and passwd1 == passwd2:
        user = User(login=login, password=generate_password_hash(passwd1))
        flash("účet vytvořen")
    else:
        flash("Hesla se neshodují nebo jsou příliš krátká")
        return redirect(url_for("adduser"))
    return redirect(url_for("index"))
######################################################################################
@app.route("/login/", methods=["GET"])
@db_session
def login():
    return render_template("login.html.j2")
######################################################################################
@app.route("/login/",methods=["POST"])
@db_session
def login_post():
    login = request.form.get("login")
    passwd = request.form.get("password")
    user = User.get(login=login)
    if user and passwd and check_password_hash(user.password, passwd):
        session["user"] = login
        flash("úspěšně jsi se přihlásil")
    else:
        flash("nesprávné přihlašovací údaje")
    return redirect(url_for("index"))
######################################################################################
@app.route("/logout/")
@db_session
def logout():
    session.pop("user", None)
    flash("Odhlášení proběhlo úspěšně")
    return render_template("base.html.j2")
######################################################################################
@app.route("/shortener/", methods=["GET"])
@login_required
@db_session
def shortener():
    return render_template("shortener.html.j2")
######################################################################################