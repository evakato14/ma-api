from . import db

class SongRating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.String(22))
    rating = db.Column(db.Integer)