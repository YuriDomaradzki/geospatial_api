
# third-party libraries
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort


blp = Blueprint("Users", __name__, description="Operations on users")


blp.route("register")

class UserRegisterResource(MethodView):

    def post(self):
        data = self.__get_json_data()

        try:
            username = data.get("username")
            password = data.get("password")
        except ValueError as ve:
            abort(400, message=str(ve))
        except IntegrityError:
            abort(409, message="An user with this credentials already exists")
        except Exception as e:
            abort(500, message=f"An error has occurred: {str(e)}")
