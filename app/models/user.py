from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db


class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(255), unique=True, nullable=False)
    picture = db.Column(db.String(500))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=True)
    refresh_token = db.Column(db.String(500), nullable=True)
    oauth_provider = db.Column(db.String, nullable=True)
    oauth_id = db.Column(db.String, nullable=True)

    playlists = db.relationship("Playlist", backref="user", lazy=True)
    history = db.relationship("ListeningHistory", backref="user", lazy=True)

    def __repr__(self) -> str:
        return f"User(name = {self.username}, email = {self.email})"

    def get_id(self):
        return str(self.id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)
