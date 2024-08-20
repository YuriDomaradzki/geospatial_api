# inbuilt libraries
import os
from pathlib import Path
from dotenv import load_dotenv

# third-party libraries
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

from flask_smorest import Api

# custom libraries
from geospatial_api.models.db import db
from geospatial_api.resources.geometry import blp as GeometryBlueprint
from geospatial_api.resources.free_geocoding import blp as FreeGeoCodingBlueprint


def create_app() -> Flask:
    """
    Creates and configures the Flask app.

    Returns
    -------
        The Flask app.
    """

    env_file_path = Path(__file__).parent / '.env'
    load_dotenv()

    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "REST API for Geospatial Data"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["SQLALCHEMY_DATABASE_URI"] = ""

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"postgresql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@"
        f"{os.getenv('DATABASE_HOST')}/{os.getenv('DATABASE_NAME')}"
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    api = Api(app)

    with app.app_context():
        db.create_all()

    # Registrando as interações dos usuários com a API
    api.register_blueprint(GeometryBlueprint)
    api.register_blueprint(FreeGeoCodingBlueprint)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)