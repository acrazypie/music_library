from flask_restful import Api
from app.api.user import *
from app.api.google_login import *
from app.api.music import *

api = Api()


def register_routes(app):
    api.init_app(app)

    api.add_resource(Users, "/api/users/")
    api.add_resource(User, "/api/users/<int:user_id>")

    api.add_resource(GoogleLogin, "auth/login")
    api.add_resource(GoogleCallback, "auth/callback")
    api.add_resource(ProtectedResource, "protected")
    api.add_resource(RefreshToken, "auth/refresh")

    api.add_resource(SongList, "/api/songs")
    api.add_resource(PlaylistList, "/api/users/<int:user_id>/playlists")
    api.add_resource(PlaylistDetail, "/api/playlists/<int:playlist_id>")
    api.add_resource(ListeningHistoryList, "/api/users/<int:user_id>/history")
