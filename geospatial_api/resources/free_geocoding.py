# inbuilt libraries
import json
from typing import Union

# third-party libraries
import requests
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from sqlalchemy import func

from flask_jwt_extended import jwt_required

from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest, Unauthorized


# 66c3523802860766751470fxoc40658

# Mapeando as interações com a API de geometrias
blp = Blueprint("FreeGeoCoding", __name__, description="Operations on FreeGeoCoding API")


@blp.route("/adresses")
class GeocodeResource(MethodView):

    def get(self):
        """
            Returns a list of addresses based on the placename parameter from the request.

        Args
        ----
            key: str,
                API key.
            placename: str,
                The placename of the address to be retrieved.
            street: str, Optional
                The street of the address to be retrieved.
            city: str, Optional
                The city of the address to be retrieved.
            county: str, Optional
                The county of the address to be retrieved.
            state: str, Optional
                The state of the address to be retrieved.
            country: str, Optional
                The country of the address to be retrieved.
            postalcode: str, Optional
                The postal code of the address to be retrieved.

        Raises
        -------
            BadRequest
                If the the parameters required are not provided.
            ValueError
                If the API key is invalid.
            LookupError
                If no data is found.

        Returns
        --------
            A list of addresses based on the placename parameter from the request.
        """

        try:
            api_key = request.args.get('key')

            if not api_key:
                raise BadRequest('Please provide an API key')

            place_name = request.args.get('placename')
            url = f'https://geocode.maps.co/search?q={place_name}&api_key={api_key}'

            if not place_name:
                street = request.args.get('street')
                city = request.args.get('city')
                county = request.args.get('county')
                state = request.args.get('state')
                country= request.args.get('country')
                postal_code = request.args.get('postalcode')

                url = f'https://geocode.maps.co/search?street={street}&city={city}'\
                      f'&state={state}&postalcode={postal_code}&country={country}&api_key={api_key}'

            response = requests.get(url)
            data = response.json()

            if response.status_code != 200:
                raise ValueError(data['message'])
            if not data:
                raise LookupError('No data found')

            return {'addresses': data}
        except (ValueError, BadRequest) as err:
            abort(400, message=str(err))
        except LookupError as le:
            abort(404, message=str(le))
        except Exception as e:
            abort(500, message=f"An error has occurred: {str(e)}")


@blp.route("/coordinates")
class CoordinatesResource(MethodView):

    def get(self):
        pass

