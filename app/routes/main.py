from flask import Blueprint


main_bp = Blueprint("main_bp", __name__)


@main_bp.route("/")
def home():
    return "<h1> Flask API</h1>"
