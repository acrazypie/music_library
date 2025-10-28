from flask_restful import Resource, Api, reqparse
from flask import jsonify
from app.models.user import UserModel
from app.models.music import Song, Playlist, PlaylistSong, ListeningHistory
from datetime import datetime
from app.api import api
from app.models import db


# --- SONGS ---
class SongList(Resource):
    def get(self):
        songs = Song.query.all()
        return jsonify(
            [
                {
                    "id": s.id,
                    "title": s.title,
                    "artist": s.artist.name if s.artist else None,
                    "genre": s.genre,
                    "duration": s.duration,
                }
                for s in songs
            ]
        )

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("title", required=True)
        parser.add_argument("artist_id", required=True, type=int)
        parser.add_argument("genre")
        parser.add_argument("duration", type=int)
        args = parser.parse_args()

        song = Song(**args)
        db.session.add(song)
        db.session.commit()
        return {"message": "Song added", "id": song.id}, 201


# --- PLAYLISTS ---
class PlaylistList(Resource):
    def get(self, user_id):
        playlists = Playlist.query.filter_by(user_id=user_id).all()
        return jsonify(
            [
                {"id": p.id, "name": p.name, "song_count": len(p.songs)}
                for p in playlists
            ]
        )

    def post(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument("name", required=True)
        args = parser.parse_args()

        playlist = Playlist()
        playlist.name = args["name"]
        playlist.user_id = user_id
        db.session.add(playlist)
        db.session.commit()
        return {"message": "Playlist created", "id": playlist.id}, 201


class PlaylistDetail(Resource):
    def get(self, playlist_id):
        playlist = Playlist.query.get_or_404(playlist_id)
        return {
            "id": playlist.id,
            "name": playlist.name,
            "songs": [
                {
                    "id": ps.song.id,
                    "title": ps.song.title,
                    "artist": ps.song.artist.name if ps.song.artist else None,
                }
                for ps in playlist.songs
            ],
        }

    def post(self, playlist_id):
        """Add song to playlist"""
        parser = reqparse.RequestParser()
        parser.add_argument("song_id", type=int, required=True)
        args = parser.parse_args()

        ps = PlaylistSong()
        ps.playlist_id = playlist_id
        ps.song_id = args["song_id"]
        db.session.add(ps)
        db.session.commit()
        return {"message": "Song added to playlist"}, 201


# --- LISTENING HISTORY ---
class ListeningHistoryList(Resource):
    def get(self, user_id):
        history = (
            ListeningHistory.query.filter_by(user_id=user_id)
            .order_by(ListeningHistory.listened_at.desc())
            .limit(20)
            .all()
        )
        return jsonify(
            [
                {
                    "song": h.song.title,
                    "artist": h.song.artist.name if h.song.artist else None,
                    "listened_at": h.listened_at.isoformat(),
                }
                for h in history
            ]
        )

    def post(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument("song_id", type=int, required=True)
        args = parser.parse_args()

        h = ListeningHistory()
        h.user_id = user_id
        h.song_id = args["song_id"]
        db.session.add(h)
        db.session.commit()
        return {"message": "Listening recorded"}, 201
