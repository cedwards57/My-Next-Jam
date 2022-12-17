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
from sptfy import get_info, get_artist_from_search, get_artist_name_from_id
from models import UserLogin, LikesArtist, db

load_dotenv(find_dotenv())


app = flask.Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL_QL")
app.secret_key = os.getenv("SECRET_KEY")
login_manager = LoginManager()
login_manager.init_app(app)
db.init_app(app)
with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return UserLogin.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized_callback():
    flask.flash("You must be logged in to view that page.")
    return flask.redirect("/")


@app.route("/")  # login GET
def enter():
    if current_user.is_authenticated:
        return flask.redirect("/userpage")
    return flask.render_template("enter.html")


@app.route("/create")  # signup GET
def create():
    if current_user.is_authenticated:
        return flask.redirect("/userpage")
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
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return flask.redirect("/userpage")


@app.route("/userpage")  # main page
@login_required
def userpage():
    artist_ids = LikesArtist.query.filter_by(username=current_user.username).all()
    my_artists = [i.artist_id for i in artist_ids]
    if my_artists == []:
        my_artists = ["x"]
        flask.flash("You don't have any artists... Add one above!")
    sptfy_data = get_info(my_artists)
    artist_names = [get_artist_name_from_id(j) for j in my_artists]
    random_song = sptfy_data["random_song"]
    return flask.render_template(
        "index.html",
        random_song=random_song,
        artist_names=artist_names,
        user=current_user.username,
        artist_ids=my_artists,
        artist_num=len(artist_names),
    )


@app.route("/songadd", methods=["POST"])
@login_required
def songadd():
    artist_name = flask.request.form["artistname"]
    artist_id = get_artist_from_search(artist_name)
    artist_exists = (
        LikesArtist.query.filter_by(
            username=current_user.username, artist_id=artist_id
        ).first()
        != None
    )
    if artist_id != "x" and artist_exists == False:
        new_artist = LikesArtist(username=current_user.username, artist_id=artist_id)
        db.session.add(new_artist)
        db.session.commit()
        flask.flash("Artist added to your list!")
    elif artist_id == "x":
        flask.flash("Sorry, that artist isn't on Spotify!")
    else:
        flask.flash("That one's already on your list!")
    return flask.redirect("/userpage")


@app.route("/songdel", methods=["POST"])
@login_required
def songdel():
    all_ids = LikesArtist.query.filter_by(username=current_user.username)
    all_ids_list = [i.artist_id for i in all_ids]
    for j in all_ids_list:
        remove_this = flask.request.form.get(j) != None
        if remove_this:
            artist_entry = LikesArtist.query.filter_by(
                username=current_user.username, artist_id=j
            ).first()
            db.session.delete(artist_entry)
    db.session.commit()
    flask.flash("Artists removed.")
    return flask.redirect("/userpage")

@app.errorhandler(Exception)
def error(e):
    flask.flash(e)
    return flask.render_template('error.html')


app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
