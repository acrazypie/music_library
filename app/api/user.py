from flask_restful import Resource, abort, marshal_with
from app.models import db
from app.models.user import UserModel
from app.utility import user_args, useFields


class Users(Resource):
    @marshal_with(useFields)
    def get(self):
        users = UserModel.query.all()
        return users


class User(Resource):
    @marshal_with(useFields)
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404)
        return user

    @marshal_with(useFields)
    def patch(self, id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404)
        user.name = args["name"]  # type: ignore
        user.email = args["email"]  # type: ignore
        db.session.commit()
        return user

    @marshal_with(useFields)
    def delete(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404)
        db.session.delete(user)
        db.session.commit()
        users = UserModel.query.all()
        return users
