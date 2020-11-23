from . import app
from flask import render_template, request, session, redirect, url_for, flash
import functools
from pony.orm import db_session
from .models import User
from werkzeug.security import check_password_hash, generate_password_hash
from uuid import uuid4

def login_required(fun):
    @functools.wraps(fun)
    def wrapper(*args, **kwargs):
        if "user" in session:
            return fun(*args, **kwargs)
        else:
            return redirect(url_for("login", url=request.path))
    return wrapper


@app.route('/login/', methods=["GET", "POST"])
@db_session
def login():
    if request.method == "POST":
        if request.form["username"] == "MOTOMOTO":
                    return redirect(url_for("moto"))
        user = User.get(login=request.form.get("username"))
        if check_password_hash(user.password,request.form.get("password")):
            session["user"] = user.login
            url = request.form["url"]
            if url != "None":
                return redirect(url)
            return redirect(url_for("index"))
        
        
    else:
        return render_template("login.html.j2", url=request.args.get("url"))

@app.route('/register/', methods=["GET","POST"])
@db_session
def register():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        password_again = request.form.get("password_again")
        if name and password == password_again:
            user = User(user_id=str(uuid4()),login=name,password=generate_password_hash(password))
            flash("Succesfuly registered")
            session["user"] = user.login
            return redirect(url_for("index"))
    return render_template("register.html.j2")


@app.route('/logout/')
def logout():
    del session["user"]
    return redirect(url_for("index"))

@app.route('/')
def index():
    pi = 3.141519
    e = 2.7
    title = 'Index'
    return render_template('base.html.j2', pi=pi, title=title)


@app.route('/info/', methods=["GET", "POST"])
def info():
    text = request.form.get("text")
    if text:
        text = text[::-1]
    else:
        text = ""
    title = 'Info'
    return render_template('info.html.j2', title=title, reversed_text=text)


@app.route('/kvetak/')
@login_required
def kvetak():
    title = "Kvetak"
    return render_template('kvetak.html.j2', title=title)


@app.route('/kapusta/')
@login_required
def kapusta():
    title = "Kapusta"
    return render_template('kapusta.html.j2', title=title)


@app.route('/banany/')
@login_required
def banany():
    title = "Banany"
    return render_template('banany.html.j2', title=title)


@app.route('/moto-secret/')
def moto():
    title = "MOTO MOTO"
    return render_template('moto.html.j2', title=title)
