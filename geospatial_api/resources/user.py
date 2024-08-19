# inbuilt libraries
from typing import Optional, List

# third-party libraries
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
)

from werkzeug.exceptions import BadRequest, Unauthorized
from sqlalchemy.exc import IntegrityError

# custom libraries
from blocklist import BLOCKLIST
from geospatial_api.models.db import db
from geospatial_api.models.user import UsersModel
from geospatial_api.utils import string_validation, string_is_alphanumeric


blp = Blueprint("Users", __name__, "Operations on users")


@blp.route("/user")
class User(MethodView):

    def __get_json_data(self) -> dict:
        """
        Gets the JSON data from the request.

        Returns
        --------
            JSON data from the request.
        """
        try:
            return request.get_json()
        except BadRequest as bre:
            abort(
                400,
                message="JSON file cannot be empty, must have username and password!",
            )

    @jwt_required()
    def get(self) -> dict:
        """
            Gets a user based on the username parameter from the request.

        Args
        ----
            username: str,
                The username of the user to be retrieved.

        Returns
        -------
            A dictionary containing the user data.
        """
        username = request.args.get('username')

        if not string_validation(text=username):
            raise ValueError(
                "The username entered for the query is in an invalid format!"
            )

        try:
            user = [
                user.as_dict()
                for user in UsersModel.query.filter_by(username=username).all()
            ]
            if not user:
                raise LookupError(f"No user with username {username}")
            return {"User": user}

        except ValueError as ve:
            abort(400, message=str(ve))
        except LookupError as le:
            abort(404, message=str(le))
        except Exception as e:
            abort(500, message=f"An error has occurred: {str(e)}")

    @jwt_required()
    def put(self) -> dict:
        """ 
            Updates a user based on the username parameter from the request.

        Args
        ----
            username: str,
                The username of the user to be updated.

        Returns
        -------
            A message indicating that the user was successfully updated.
        """
        username = request.args.get('username')

        data = self.__get_json_data()
        keys = data.keys()
        try:
            new_username = data.get("new_username") if "new_username" in keys else ""
            new_password = data.get("new_password") if "new_password" in keys else ""

            user = UsersModel.query.filter_by(username=username).first()

            if not user:
                raise LookupError(f"No user with username {username}")

            if new_username:
                user.username = new_username
            if new_password:
                user.password = pbkdf2_sha256.hash(new_password)

            db.session.commit()
            db.session.close()

            return {"Sucess": "The user was updated with successfully"}

        except ValueError as ve:
            abort(400, message=str(ve))
        except LookupError as le:
            abort(404, message=str(le))
        except Exception as e:
            abort(500, message=f"An error has occurred: {str(e)}")

    @jwt_required()
    def delete(self) -> dict:
        """ 
            Deletes a user based on the username parameter from the request.

        Args
        ----
            username: str,
                The username of the user to be deleted.

        Returns
        -------
            A message indicating that the user was successfully deleted.
        """
        data = self.__get_json_data()
        keys = data.keys()

        username = request.args.get('username')

        try:
            user = UsersModel.query.filter_by(username=username).first()

            if not user:
                raise LookupError(f"No user with username {username}")

            db.session.delete(user)
            db.session.commit()
            db.session.close()

            return {"Success": "The user was deleted successfully"}, 200

        except ValueError as ve:
            abort(400, message=str(ve))
        except LookupError as le:
            abort(404, message=str(le))
        except Exception as e:
            abort(
                500,
                message=f"An error has occurred: Check if the username you want to delete is correct.",
            )


@blp.route("/register")
class UserRegister(MethodView):

    def __get_json_data(self) -> dict:
        """
        Gets the JSON data from the request.

        Returns
        --------
            JSON data from the request.
        """
        try:
            return request.get_json()
        except BadRequest as bre:
            abort(
                400,
                message="JSON file cannot be empty, must have username and password!",
            )


    def __validate_keys(
        self, data: dict, keys: Optional[List] = ["username", "password"]
    ) -> None:
        """
        Validates that the required keys are present in the data.

        Parameters
        ----------
            data: str,
                Data to be validated.
            keys: Optional[List],
                List of required keys. Default is ['username', 'password'].
        """
        try:
            valid_keys = all(
                key.lower() in [k.lower() for k in data.keys()] for key in keys
            )
            if not valid_keys:
                raise BadRequest(
                    f"You must provide the following keys: {', '.join(keys)}"
                )
        except BadRequest as bre:
            abort(400, message=str(bre))


    def post(self) -> dict:
        """
            Adds a new user to the database.

        Returns
        -------
            A message indicating that the user was added successfully.
        """
        data = self.__get_json_data()
        self.__validate_keys(data=data)

        try:
            username = data.get("username")
            password = data.get("password")

            if not string_is_alphanumeric(text=username):
                raise ValueError("The username entered for is in an invalid format!")

            if UsersModel.verify_username(username=username):
                raise IntegrityError(f"User with username '{username}' already exists.")

            user = UsersModel(
                username=username,
                password=pbkdf2_sha256.hash(password),
            )

            db.session.add(user)
            db.session.commit()
            db.session.close()

            return {"Success": f"User {username} added!"}, 201

        except ValueError as ve:
            abort(400, message=str(ve))
        except IntegrityError:
            abort(409, message="An user with this credentials already exists")
        except Exception as e:
            abort(500, message=f"An error has occurred: {str(e)}")


@blp.route("/login")
class UserLogin(MethodView):

    def __get_json_data(self) -> dict:
        """
        Gets the JSON data from the request.

        Returns
        --------
            JSON data from the request.
        """
        try:
            return request.get_json()
        except BadRequest as bre:
            abort(
                400,
                message="JSON file cannot be empty, must have username and password!",
            )

    def __validate_keys(
        self, data: dict, keys: Optional[List] = ["username", "password"]
    ) -> None:
        """
            Validates that the required keys are present in the data.

        Parameters
        ----------
            data: str,
                Data to be validated.
            keys: Optional[List],
                List of required keys. Default is ['username', 'password'].
        """
        try:
            valid_keys = all(
                key.lower() in [k.lower() for k in data.keys()] for key in keys
            )
            if not valid_keys:
                raise BadRequest(
                    f"You must provide the following keys: {', '.join(keys)}"
                )
        except BadRequest as bre:
            abort(400, message=str(bre))

    def post(self) -> dict:
        """
            Checks if the user exists and if the password is correct.

        Returns
        -------
            An access token if the credentials are correct, otherwise returns an error
            with an unauthorized message.
        """
        data = self.__get_json_data()
        self.__validate_keys(data=data)

        try:
            username = data.get("username")
            password = data.get("password")

            if not string_is_alphanumeric(text=username):
                raise ValueError("The username entered for is in an invalid format!")

            user = UsersModel.query.filter_by(username=username).first()

            if user and pbkdf2_sha256.verify(password, user.password):
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(identity=user.id)
                return {"access_token": access_token, "refresh_token": refresh_token}
            raise Unauthorized("Invalid credentials")

        except ValueError as ve:
            abort(400, message=str(ve))
        except Unauthorized as un:
            abort(401, message=str(un))
        except Exception as e:
            abort(500, message=f"An error has occurred: {str(e)}")


@blp.route("/refresh")
class UserLoginRefresh(MethodView):

    @jwt_required(refresh=True)
    def post(self) -> dict:
        """
            Refreshes the access token.

        Returns
        -------
            A new access token to refresh the user's session.
        """
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}


@blp.route("/logout")
class UserLogout(MethodView):

    @jwt_required()
    def post(self) -> dict:
        """ 
            Logs out the user.

        Returns
        -------
            A message indicating that the user was successfully logged out.
        """
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out."}