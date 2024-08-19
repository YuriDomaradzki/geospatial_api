
# third-party libraries
import requests
from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from flask_jwt_extended import jwt_required

from werkzeug.exceptions import BadRequest


# Mapeando as interações com a API de geometrias
blp = Blueprint("FreeGeoCoding", __name__, description="Operations on FreeGeoCoding API")


@blp.route("/adresses")
class GeocodeResource(MethodView):

    def get(self) -> dict:
        """
        Returns a list of addresses based on the placename or other optional parameters.

        This method uses the provided parameters to make a request to a geocoding service 
        and returns a list of addresses that match the search criteria.

        Args
        ----
            key : str
                API key for accessing the geocoding service.
            placename : str
                The placename of the address to be retrieved.
            street : str, Optional
                The street of the address to be retrieved.
            city : str, Optional
                The city of the address to be retrieved.
            county : str, Optional
                The county of the address to be retrieved.
            state : str, Optional
                The state of the address to be retrieved.
            country : str, Optional
                The country of the address to be retrieved.
            postalcode : str, Optional
                The postal code of the address to be retrieved.

        Returns
        -------
            dict
                A dictionary containing a list of addresses that match the search criteria.

        Raises
        ------
            BadRequest
                If the API key or placename is missing or invalid.
            LookupError
                If no data is found for the provided search criteria.
            Exception
                For any other errors that occur during the request.
        """
        try:

            try:
                data = request.get_json()
            except BadRequest:
                raise BadRequest('Please provide a JSON payload in the request body')

            api_key = data.get('api_key')
            if not api_key:
                raise BadRequest('Please provide an API key in the request body')

            place_name = request.args.get('placename')
            if not place_name:
                street = request.args.get('street')
                city = request.args.get('city')
                state = request.args.get('state')
                country= request.args.get('country')
                postal_code = request.args.get('postalcode')

                if not all([street, city, state, country, postal_code]):
                    raise BadRequest('Please provide all required search parameter')

                url = f'https://geocode.maps.co/search?street={street}&city={city}'\
                      f'&state={state}&postalcode={postal_code}&country={country}&api_key={api_key}'
            else:
                url = f'https://geocode.maps.co/search?q={place_name}&api_key={api_key}'

            response = requests.get(url)
            if response.status_code != 200:
                abort(response.status_code, description='Error from geocoding service')

            data = response.json()
            if not data:
                raise LookupError('No data found')

            return jsonify({'adresses': data})

        except BadRequest as bre:
            abort(400, message=str(bre))
        except LookupError as le:
            abort(404, message=str(le))
        except Exception as e:
            abort(500, description=f'An unexpected error has occurred: {str(e)}')


@blp.route("/coordinates")
class CoordinatesResource(MethodView):

    def get(self) -> dict:
        """
        Retrieves the address information based on latitude and longitude parameters.

        This method uses the latitude and longitude provided as query parameters 
        to make a request to a geocoding service and returns the corresponding address information.

        Args
        ----
            key : str
                API key for accessing the geocoding service.
            lat : float
                The latitude for the location to retrieve.
            lon : float
                The longitude for the location to retrieve.

        Returns
        -------
            dict
                A dictionary containing the address information based on the provided coordinates.

        Raises
        ------
            BadRequest
                If the API key, latitude, or longitude are missing or invalid.
            Exception
                For any other errors that occur during the request.
        """
        try:
            data = request.get_json() or {}
            api_key = data.get('api_key')
            if not api_key:
                raise BadRequest('Please provide an API key in the request body')

            lat = request.args.get('lat')
            lon = request.args.get('lon')
            if not lat or not lon:
                raise BadRequest('Please provide latitude and longitude')

            try:
                lat = float(lat)
                lon = float(lon)
            except ValueError:
                abort(400, description='Latitude and longitude must be valid numbers')

            url = f'https://geocode.maps.co/reverse?lat={lat}&lon={lon}&api_key={api_key}'

            response = requests.get(url)

            if response.status_code != 200:
                abort(response.status_code, description='Error from geocoding service')

            data = response.json()
            if not data:
                raise LookupError('No data found')

            return jsonify({'coordinates': data})

        except BadRequest as bre:
            abort(400, message=str(bre))
        except LookupError as le:
            abort(404, message=str(le))
        except Exception as e:
            abort(500, description=f'An unexpected error has occurred: {str(e)}')

