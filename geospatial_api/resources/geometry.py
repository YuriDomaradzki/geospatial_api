# inbuilt libraries
import json
from typing import Union

# third-party libraries
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from sqlalchemy import func

from werkzeug.exceptions import BadRequest, Unauthorized, UnsupportedMediaType

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
            Creates a new geometry based on the description and geom parameters extracted from
            the JSON payload of the request.

            The method expects a JSON payload with 'description' and 'geom' keys. It validates the inputs
            and then inserts a new geometry into the database.

        Returns
        -------
            dict
                A dictionary with a success message.

        Raises
        ------
            ValueError
                If 'description' or 'geom' are not provided or if 'geom' is not a valid GeoJSON object.
            BadRequest
                If the JSON payload is empty or malformed.
            Exception
                For any other server-side errors.
        """
        try:

            data = request.get_json()

            description = data.get('description')
            geom = data.get('geom')

            # Verifica se os parâmetros description e geom foram fornecidos e se
            # o geom é um objeto GeoJSON
            if not description or not geom:
                raise ValueError("Please provide description or geom")
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
            message = "JSON file cannot be empty, must have description and geom!"
            abort(400, message=message)
        except LookupError as le:
            abort(404, message=str(le))
        except UnsupportedMediaType as ume:
            abort(415, message=str(ume))
        except Exception as e:
            abort(500, message=f"An error has occurred: {str(e)}")


    def get(self) -> dict:
        """
            Retrieves a list of geometries from the database.

            This method can retrieve a specific geometry by its ID, passed as a query parameter,
            or a list of geometries that match the provided filters ('description' and 'geom') in the
            JSON body of the request.

            If no ID is provided, the method filters geometries based on the optional 'description'
            and 'geom' fields. The 'geom' field should be in GeoJSON format.

        Returns
        -------
            dict
                A list of geometries matching the criteria, or an error message if no geometries are found.

        Raises
        ------
            ValueError
                If the 'description' and 'geom' parameters are missing or invalid.
            BadRequest
                If the request body is empty or not a valid JSON.
            LookupError
                If no geometry is found with the given ID or matching the filters.
            UnsupportedMediaType
                If the request content type is not supported.
            Exception
                For any other server-side errors.
        """
        try:
            id = request.args.get('id')

            # Busca pelo ID
            if id:
                geometry = db.session.get(GeometryModel, id)
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

            geometry = db.session.query(GeometryModel)

            if geom:
                geom_json = json.dumps(geom)
                geom = func.ST_GeomFromGeoJSON(geom_json)
                geometry = geometry.filter(func.ST_Contains(GeometryModel.geom, geom))
                #geometry = geometry.filter(func.ST_Contains(GeometryModel.geom, geom))

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
        except UnsupportedMediaType as ume:
            abort(415, message=str(ume))
        except Exception as e:
            abort(500, message=f"An error has occurred: {str(e)}")


    def put(self) -> dict:
        """
            Updates an existing geometry based on the provided ID.

            This method updates the 'description' and/or 'geom' fields of a geometry 
            identified by the given ID, which is passed as a query parameter. 
            The 'geom' field should be in GeoJSON format.

            If the ID is not found in the database, a 404 error is returned.

        Returns
        -------
            dict
                A message indicating that the geometry was successfully updated.

        Raises
        ------
            ValueError
                If the request body is empty or the data is invalid.
            BadRequest
                If the ID parameter is missing or the JSON data is invalid.
            LookupError
                If no geometry is found with the given ID.
            Exception
                For any other server-side errors.
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

            geometry = db.session.get(GeometryModel, id)
            if not geometry:
                raise LookupError(f"No geometry with id {id}")

            if new_description:
                geometry.description = new_description
            if new_geom:
                geometry.geom = func.ST_GeomFromGeoJSON(json.dumps(new_geom))

            db.session.commit()

            return {"Success": "The geometry was updated successfully"}, 200
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
            Deletes a geometry from the database based on the provided ID.

            This method deletes a geometry identified by the given ID, which is passed as 
            a query parameter. If the ID is not found, a 404 error is returned.

        Returns
        -------
            dict
                A message indicating that the geometry was successfully deleted.

        Raises
        ------
            BadRequest
                If the ID parameter is missing.
            LookupError
                If no geometry is found with the given ID.
            Exception
                For any other server-side errors.
        """
        try:
            id = request.args.get('id')

            # Verificar se o parâmetro id foi fornecido
            if not id:
                abort(400, message="Please provide an id")

            geometry = db.session.get(GeometryModel, id)

            if not geometry:
                raise LookupError(f"No geometry found with id {id}")

            db.session.delete(geometry)
            db.session.commit()
            db.session.close()

            return {"Sucess": f"The geometry with id {id} was deleted with successfully"}, 200
        except ValueError as ve:
            abort(400, message=str(ve))
        except BadRequest as bre:
            message = "JSON file cannot be empty, must have description and geom!"
            abort(400, message=message)
        except LookupError as le:
            abort(404, message=str(le))
        except Exception as e:
            abort(500, message=f"An error has occurred: {str(e)}")

