from datetime import datetime
from app.models import db


class Artist(db.Model):
    __tablename__ = "artists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    albums = db.relationship("Album", backref="artist", lazy=True)
    songs = db.relationship("Song", backref="artist", lazy=True)


class Album(db.Model):
    __tablename__ = "albums"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable=False)
    songs = db.relationship("Song", backref="album", lazy=True)


class Song(db.Model):
    __tablename__ = "songs"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    duration = db.Column(db.Integer)
    genre = db.Column(db.String(100))
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey("albums.id"), nullable=True)


class Playlist(db.Model):
    __tablename__ = "playlists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    songs = db.relationship(
        "PlaylistSong", backref="playlist", lazy=True, cascade="all, delete-orphan"
    )


class PlaylistSong(db.Model):
    __tablename__ = "playlist_songs"
    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey("playlists.id"), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey("songs.id"), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    song = db.relationship("Song")


class ListeningHistory(db.Model):
    __tablename__ = "listening_history"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey("songs.id"), nullable=False)
    listened_at = db.Column(db.DateTime, default=datetime.now())
    song = db.relationship("Song")
