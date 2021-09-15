import os
import flask
from sptfy import get_info

app = flask.Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/")
def index():
    sptfy_data = get_info()
    random_song = sptfy_data["random_song"]
    return flask.render_template(
        "index.html",
        random_song = random_song
    )


app.run()

# app.run(
#     host="0.0.0.0",
#     port=int(os.getenv("PORT", "8080"))
# )
