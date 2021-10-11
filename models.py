from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class UserLogin(db.Model, UserMixin):
    username = db.Column(db.String(15), primary_key="True")
    password = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        return "<UserLogin %r %r>" % (self.username, self.password)

    def get_id(self):
        return self.username


class LikesArtist(db.Model):
    username = db.Column(db.String(15), primary_key="True")
    artist_id = db.Column(db.String(80), primary_key="True")

    def __repr__(self):
        return "<LikesArtist %r %r>" % (self.username, self.artist_id)
