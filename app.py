import os
import flask
import random
from sptfy import get_info

app = flask.Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/")
def index():
    sptfy_data = get_info()
    releases = sptfy_data["releases"]
    songs = sptfy_data["all_songs"]
    return flask.render_template(
        "index.html",
        releases = releases,
        songs = songs,
        random_song = random.choice(songs)
    )

app.run(
    host="0.0.0.0",
    port=int(os.getenv("PORT", "8080"))
)
