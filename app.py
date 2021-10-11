import os
from dotenv import find_dotenv, load_dotenv
import flask
from flask_login import (
    LoginManager,
    login_required,
    current_user,
    login_user,
    logout_user,
)
from sptfy import get_info
from models import UserLogin, LikesArtist, db
from flask_sqlalchemy import SQLAlchemy

load_dotenv(find_dotenv())
# testuser1, xyz
# userone, testone

app = flask.Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.secret_key = os.getenv("SECRET_KEY")
login_manager = LoginManager()
login_manager.init_app(app)
db.init_app(app)
with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return UserLogin.query.get(user_id)


@app.route("/")  # login GET
def enter():
    return flask.render_template("enter.html")


@app.route("/create")  # signup GET
def create():
    return flask.render_template("create.html")


@app.route("/login", methods=["POST"])  # login POST
def login():
    entered_name = flask.request.form["username"]
    entered_pw = flask.request.form["password"]
    this_user = UserLogin.query.filter_by(username=entered_name).first()
    if not this_user or (this_user.password != entered_pw):
        flask.flash("Incorrect username or password.")
        return flask.redirect("/")
    else:
        login_user(this_user)
        return flask.redirect("/userpage")


@app.route("/logout")  # logout POST
@login_required
def logout():
    logout_user()
    return flask.redirect("/")


@app.route("/signup", methods=["POST"])  # signup POST
def signup():
    entered_name = flask.request.form["username"]
    entered_pw = flask.request.form["password"]
    this_user = UserLogin.query.filter_by(username=entered_name).first()

    if this_user:
        flask.flash("This username is taken.")
        return flask.redirect("/create")
    else:
        new_user = UserLogin(username=entered_name, password=entered_pw)
        print(new_user)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return flask.redirect("/userpage")


@app.route("/userpage")  # main page
@login_required
def userpage():
    sptfy_data = get_info()
    random_song = sptfy_data["random_song"]
    return flask.render_template("index.html", random_song=random_song)


app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
