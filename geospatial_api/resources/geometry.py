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
            id = request.args.get('id')

            # Busca pelo ID
            if id:
                geometry = GeometryModel.query.get(id)
                if not geometry:
                    raise LookupError(f"No geometry found with id {id}")
                return [geometry.as_dict()]

            # Se não houver ID, busca por parâmetros de filtro
            data = request.get_json()
            if not data:
                raise BadRequest("Request body must contain JSON data.")

            description = data.get('description')
            geom = data.get('geom')

            if not self.__validate_parameters(description=description, geom=geom):
                raise ValueError("Invalid parameters: description and geom are required.")

            geometry = GeometryModel.query

            if geom:
                geom_json = json.dumps(geom)
                geom = func.ST_GeomFromGeoJSON(geom_json)
                geometry = geometry.filter(func.ST_Contains(GeometryModel.geom, geom))

            if description:
                geometry = geometry.filter_by(description=description)

            geoms = [geo.as_dict() for geo in geometry.all()]

            if not geoms:
                raise LookupError("No geometry found.")

            return geoms
        except ValueError as ve:
            abort(400, message=str(ve))
        except BadRequest as bre:
            message = "JSON file cannot be empty, must have description and geom!"
            abort(400, message=message)
        except LookupError as le:
            abort(404, message=str(le))
        except Exception as e:
            abort(500, message=f"An error has occurred: {str(e)}")


    def put(self) -> dict:
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
        try:
            data = request.get_json()
            if not data:
                raise ValueError("The request body must contain data.")

            id = request.args.get('id')

            # Verificar se o parâmetro id foi fornecido
            if not id:
                abort(400, message="Please provide an id")

            new_description = data.get("new_description", "")
            new_geom = data.get("new_geom", "")

            geometry = GeometryModel.query.get(id)
            if not geometry:
                raise LookupError(f"No geometry with id {id}")

            if new_description:
                geometry.description = new_description
            if new_geom:
                geometry.geom = func.ST_GeomFromGeoJSON(json.dumps(new_geom))

            db.session.commit()

            return {"Success": "The geometry was updated successfully"}, 201
        except ValueError as ve:
            abort(400, message=str(ve))
        except BadRequest as bre:
            message = "JSON file cannot be empty, must have description and geom!"
            abort(400, message=message)
        except LookupError as le:
            abort(404, message=str(le))
        except Exception as e:
            abort(500, message=f"An error has occurred: {str(e)}")


    def delete(self) -> dict:
        """
            Deletes a geometry based on the id parameter.

        Args
        ----
            id: int,
                ID of the geometry

        Returns
        -------
            A message indicating that the geometry was successfully deleted.
        """
        try:
            id = request.args.get('id')

            # Verificar se o parâmetro id foi fornecido
            if not id:
                abort(400, message="Please provide an id")

            geometry = GeometryModel.query.get(id)

            db.session.delete(geometry)
            db.session.commit()
            db.session.close()

            return {"Sucess": f"The geometry with id {id} was deleted with successfully"}, 200
        except ValueError as ve:
            abort(400, message=str(ve))
        except BadRequest as bre:
            message = "JSON file cannot be empty, must have description and geom!"
            abort(400, message=message)
        except Exception as e:
            abort(500, message=f"An error has occurred: {str(e)}")
