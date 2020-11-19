from . import app
from flask import render_template, request, redirect, url_for, session
import functools

# from werkzeug.security import check_password_hash


def login_required(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        if "user" in session:
            return function(*args, **kwargs)
        else:
            return redirect(url_for("login", url=request.path))

    return wrapper


@app.route("/", methods=["GET"])
def index():
    return render_template("base.html.j2")


@app.route("/<string:shortcut>", methods=["GET"])
def short_redirect(shortcut):
    return render_template("base.html.j2")


@app.route("/adduser/")
def adduser():
    return render_template("base.html.j2")


@app.route("/login/")
def login():
    return render_template("login.html.j2")


@app.route("/logout/")
def logout():
    return render_template("base.html.j2")
