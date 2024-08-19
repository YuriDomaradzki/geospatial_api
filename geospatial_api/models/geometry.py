# third-party libraries
from geoalchemy2 import Geometry

# custom libraries
from geospatial_api.models.db import db


class GeometryModel(db.Model):

    __tablename__ = 'geometries'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    geom = db.Column(Geometry(geometry_type='GEOMETRY', srid=4326), nullable=False)

    def as_dict(self) -> dict:
        """
        Returns a dictionary representation of the Geometry object.

        Returns
        -------
            A dictionary representation of the Geometry object.
        """
        return {
            "ID": self.id,
            "DESCRIPTION": self.description,
            "GEOMETRY": str(self.geom)
        }