from flask import Flask
from authlib.integrations.flask_client import OAuth
from flask_login import LoginManager
from app.api import register_routes
from app.models import db
from app.models.user import UserModel
from app.routes.main import main_bp
from .utility import config

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.secret_key = config.SECRET_KEY or "dev"

login_manager = LoginManager(app)
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))


oauth = OAuth(app)

# Google (OpenID Connect)
oauth.register(
    name="google",
    client_id=config.GOOGLE_CLIENT_ID,
    client_secret=config.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

db.init_app(app)

register_routes(app)

app.register_blueprint(main_bp)
