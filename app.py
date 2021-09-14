import os
import flask
from sptfy import get_releases

app = flask.Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/")
def hello_world():
    release_data = get_releases()
    releases = release_data["releases"]
    return flask.render_template(
        "index.html",
        releases = releases
    )

app.run(
    host="0.0.0.0",
    port=int(os.getenv("PORT", "8080"))
)
