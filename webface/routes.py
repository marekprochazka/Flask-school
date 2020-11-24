from . import app
from flask import render_template, request, session, redirect, url_for, flash
import functools
from pony.orm import db_session, select
from .models import User,Shortener
from werkzeug.security import check_password_hash, generate_password_hash
from uuid import uuid4
from .utils import generate_short_url


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
        user = User.get(username=request.form.get("username"))
        if user:
            if check_password_hash(user.password,request.form.get("password")):
                session["user"] = user.username
                url = request.form["url"]
                if url != "None":
                    return redirect(url)
                return redirect(url_for("index"))
            else:
                session.pop('_flashes', None)
                flash("Špatné heslo")
                return render_template("login.html.j2", url=request.args.get("url"))
        else:
            session.pop('_flashes', None)
            flash("Neplatné uživatelské jméno")
            return render_template("login.html.j2", url=request.args.get("url"))
        
        
    else:
        return render_template("login.html.j2", url=request.args.get("url"))

@app.route('/register/', methods=["GET","POST"])
@db_session
def register():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        password_again = request.form.get("password_again")
        if name:
            if not User.get(username=name):
                if password == password_again:
                    user = User(user_id=str(uuid4()),username=name,password=generate_password_hash(password))
                    session.pop('_flashes', None)
                    flash("Succesfuly registered")
                    session["user"] = user.username
                    return redirect(url_for("index"))
                else:
                    session.pop('_flashes', None)
                    flash("Hesla se musí shodovat")
                    return render_template("register.html.j2")

            else:
                session.pop('_flashes', None)
                flash("Uživatelské jméno již existuje")
                return render_template("register.html.j2")

        else:
            session.pop('_flashes', None)
            flash("Je nutné zadat jméno")
            return render_template("register.html.j2")
            
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

@app.route("/s/",methods=["GET","POST"])
@db_session
def shortener():
    if request.method == "POST":
        url = request.form.get("url")
        username = session.get("user")
        user = User.get(username=username) if username else None
        q = list(select(e for e in Shortener  
                                if e.url == url ))
        existing = q[0] if q else None
        if existing:
            if user:
                if existing.user == user:
                    return render_template("shortener.html.j2",shortcut=existing.shortcut)
                else:
                    Shortener(shortened_id=str(uuid4()),shortcut=existing.shortcut,url=url,user=user)
                    return render_template("shortener.html.j2",shortcut=existing.shortcut)
            else:
                    return render_template("shortener.html.j2",shortcut=existing.shortcut)


        else:
            shorts = list(Shortener.select())
            shorts = [short.shortcut for short in shorts]
            new_short = generate_short_url(shorts)
            if user:
                Shortener(shortened_id=str(uuid4()),shortcut=new_short,url=url,user=user)
            else: 
                Shortener(shortened_id=str(uuid4()),shortcut=new_short,url=url)
            return render_template("shortener.html.j2",shortcut=new_short)
    return render_template("shortener.html.j2")


@app.route("/s/<string:short>")
@db_session
def shortened(short):
    if session["user"]:
        shortened_object = Shortener.get(shortcut=short,user=User.get(username=session["user"]))
        if not shortened_object:
            shortened_object = Shortener.get(shortcut=short)
    else:
        shortened_object = Shortener.get(shortcut=short)
    return redirect(shortened_object.url)
    
    
