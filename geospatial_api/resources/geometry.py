# inbuilt libraries
import json
from typing import Union

# third-party libraries
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from sqlalchemy import func

from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest, Unauthorized

# custom libraries
from geospatial_api.models.db import db
from geospatial_api.models.geometry import GeometryModel


# Mapeando as interações com a API de geometrias
blp = Blueprint("Geometry", __name__, description="Operations on geometries")


@blp.route("/geometry")
class GeometryResource(MethodView):


    @staticmethod
    def __validate_parameters(description: str, geom: dict) -> Union[bool, ValueError]:
        """
            Verifica se os parâmetros description e geom foram fornecidos e se 
            o geom é um objeto GeoJSON.

        Args
        ----
            description: str,
                Description of the geometry
            geom: dict,
                Geometry in GeoJSON format

        Returns
        -------
            True if the parameters are valid, ValueError exception otherwise
        """
        # Retorna um erro 400 indicando que description ou geom devem ser fornecidos
        if not description and not geom:
            raise ValueError("Please provide description or geom")

        # Retorna um erro 400 indicando que geom deve ser um objeto GeoJSON
        if geom and not isinstance(geom, dict):
            raise ValueError("Geom should be a GeoJSON object")

        return True


    def post(self) -> dict: 
        """
            Creates a new geometry based on the description and geom parameters.

        Args
        ----
            description: str,
                Description of the geometry
            geom: dict,
                Geometry in GeoJSON format

        Returns
        -------
            A message indicating that the geometry was successfully added.
        """
        try:

            data = request.get_json()

            description = data.get('description')
            geom = data.get('geom')

            # Verifica se os parâmetros description e geom foram fornecidos e se
            # o geom é um objeto GeoJSON
            if self.__validate_parameters(description=description, geom=geom):
                geom = GeometryModel(
                    description=description,
                    geom=func.ST_GeomFromGeoJSON(json.dumps(geom)) 
                )

                db.session.add(geom)
                db.session.commit()
                db.session.close()

                return {"Success": f"Geometry added!"}, 201
        except ValueError as ve:
            abort(400, message=str(ve))
        except BadRequest as bre:
            abort(400,
                message="JSON file cannot be empty, must have description and geom!")
        except IntegrityError:
            abort(409, message="An geometry with this description and geometry already exists")
        except Exception as e:
            abort(500, message=f"An error has occurred: {str(e)}")


    def get(self) -> dict:
        """
            Returns a list of geometries based on the description and geom parameters.

        Args
        ----
            description: str,
                Description of the geometry
            geom: dict,
                Geometry in GeoJSON format

        Returns
        -------
            A list of geometries that match the description and geom parameters.
        """

        try:
            description = request.args.get('description')
            geom = request.args.get('geom')

            # Verifica se os parâmetros description e geom foram fornecidos e se
            # o geom é um objeto GeoJSON
            if self.__validate_parameters(description=description, geom=geom):
                if description and not geom:
                    geoms = [geom.as_dict() for geo in GeometryModel.query.filter_by(description=
                                                                            description).all()]
                else:
                    geom = func.ST_GeomFromGeoJSON(geom)
                    if geom and not description:
                        geoms = [geom.as_dict() for geo in GeometryModel.query.filter_by(
                                                            func.ST_Contains(GeometryModel.geom, 
                                                            geom)).all()]
                    else:
                        geoms = [geom.as_dict() for geo in GeometryModel.query.filter_by(
                                                            func.ST_Contains(GeometryModel.geom, 
                                                            geom)).filter_by(description=
                                                            description).all()]
                if not geoms:
                    raise LookupError("No geometry found!")
                return geoms
        except ValueError as ve:
            abort(400, message=str(ve))
        except LookupError as le:
            abort(404, message=str(le))
        except Exception as e:
            abort(500, message=f"An error has occurred: {str(e)}")


    def put(self):
        """
            Creates a new geometry based on the description and geom parameters.

        Args
        ----
            description: str,
                Description of the geometry
            geom: dict,
                Geometry in GeoJSON format

        Returns
        -------
            A message indicating that the geometry was successfully updated.
        """
        data = self.__get_json_data()

        try:
            description = data.get('description')
            geom = data.get('geom')

            # Verifica se os parâmetros description e geom foram fornecidos e se
            # o geom é um objeto GeoJSON
            if self.__validate_parameters(description=description, geom=geom):
                new_description = data.get("new_description") if "new_description" in keys else ""
                new_geom = data.get("new_geom") if "new_geom" in keys else ""

                geometry = GeometryModel.query.filter_by(func.ST_Contains(GeometryModel.geom, 
                                                        geom)).first()

                if new_description:
                    geometry.description = new_description
                if new_geom:
                    geometry.geom = func.ST_GeomFromGeoJSON(geom)

                db.session.commit()
                db.session.close()

                return {"Sucess": "The geometry was updated with successfully"}
        except ValueError as ve:
            abort(400, message=str(ve))
        except IntegrityError:
            abort(409, message="An geometry with this description and geometry already exists")
        except Exception as e:
            abort(500, message=f"An error has occurred: {str(e)}")


    def delete(self):
        data = self.__get_json_data()

        try:
            description = data.get('description')
            geom = data.get('geom')

            geometry = GeometryModel.query.filter_by(func.ST_Contains(GeometryModel.geom, 
                                                     geom)).filter_by(description=description).first()
            print(geometry)

            """db.session.delete(user)
            db.session.commit()
            db.session.close()"""
        except ValueError as ve:
            abort(400, message=str(ve))
        except IntegrityError:
            abort(409, message="An geometry with this description and geometry already exists")
        except Exception as e:
            abort(500, message=f"An error has occurred: {str(e)}")
