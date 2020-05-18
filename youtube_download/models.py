from youtube_download import db


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    url = db.Column(db.String(120), nullable=False)