# custom libraries
from geospatial_api.models.db import db


class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    def as_dict(self) -> dict:
        """
        Returns a dictionary representation of the Geometry object.

        Returns
        -------
            A dictionary representation of the Geometry object.
        """
        return {
            "ID": self.id,
            "USERNAME": self.username
        }

    @classmethod
    def verify_username(cls, username: str) -> bool:
        """
        Checks if a username already exists in the database.

        Parameters
        ----------
            username: str,
                the username to be checked.

        Returns
        -------
            Returns True if the username already exists, otherwise returns False.
        """
        existing_user = cls.query.filter_by(USERNAME=username).first()
        if existing_user:
            return True
        return False

