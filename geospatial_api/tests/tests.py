import sys
import os
import unittest
from pathlib import Path
from dotenv import load_dotenv
from geospatial_api.app import create_app
from geospatial_api.models.db import db

class TestGeometryResource(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
            Set up the test client and app context. This method is called before any test case is run.
        """
        cls.base_url = "http://127.0.0.1:5000/"

        env_file_path = Path(__file__).resolve().parent.parent.parent / '.env'

        if not env_file_path.exists():
            raise FileNotFoundError(f"No .env file found at {env_file_path}. It's required to run this app.")

        load_dotenv(dotenv_path=env_file_path)

        try:
            cls.app = create_app()
            cls.app.config['TESTING'] = True
            cls.app.config['SQLALCHEMY_DATABASE_URI'] = (
                f"postgresql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@"
                f"{os.getenv('DATABASE_HOST')}/{os.getenv('DATABASE_NAME')}"
            )

            cls.client = cls.app.test_client()

            with cls.app.app_context():
                db.create_all()
        except Exception as e:
            print(f"Error in setUpClass: {e}")
            raise

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests."""
        with cls.app.app_context():
            db.drop_all()

    def setUp(self):
        """Setup for individual tests."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.create_all()

    def tearDown(self):
        """Cleanup after individual tests."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # ---------------------------------------------------------------------------
    # TESTING POST GEOMETRY
    # ---------------------------------------------------------------------------
    def test_post_valid_geometry(self):
        """
            Test if the API returns a 201 response when the geometry is successfully posted.

        Returns
        -------
                A 201 response if the geometry is successfully updated in the database.
        """
        data = {
            "description": "My new geometry",
            "geom": {
                "type": "Point",
                "coordinates": [-73.935242, 40.73061]
            }
        }
        response = self.client.post(f'{self.base_url}geometry', json=data)
        self.assertEqual(response.status_code, 201)

    def test_post_none_field_information(self):
        """
            Test if the API returns a 415 response when the geometry is successfully posted
            with no field information provided.

        Returns
        -------
            A 415 response if the geometry is successfully updated in the database.
        """

        response = self.client.post(f'{self.base_url}geometry')
        self.assertEqual(response.status_code, 415)

    def test_post_invalid_field_information(self):
        """ 
            Test if the API returns a 400 response when the geometry is successfully posted
            with invalid field information provided.

        Returns
        -------
            A 400 response if the geometry is successfully updated in the database.
        """
        data = {
            "description": "My new geometry"
        }
        response = self.client.post(f'{self.base_url}geometry', json=data)
        self.assertEqual(response.status_code, 400)

    # ---------------------------------------------------------------------------
    # TESTING GET GEOMETRY
    # ---------------------------------------------------------------------------
    def test_geometry_with_valid_id(self):
        """ 
            Test if the API returns a 200 response when the geometry is successfully retrieved
            with a valid ID.

        Returns
        -------
            A 200 response if the geometry is successfully retrieved from the database.
        """ 
        self.test_post_valid_geometry()
        response = self.client.get(f'{self.base_url}geometry?id=1')
        self.assertEqual(response.status_code, 200)

    def test_geometry_with_blank_id(self):
        """
            Test if the API returns a 415 response when the geometry is successfully retrieved
            with a blank ID. 

        Returns
        -------
            A 415 response if the geometry is successfully retrieved from the database.
        """
        response = self.client.get(f'{self.base_url}geometry?id=')
        self.assertEqual(response.status_code, 415)

    def test_geometry_with_invalid_id(self):
        """ 
            Test if the API returns a 500 response when the geometry is successfully retrieved
            with an invalid ID.

        Returns
        -------
            A 500 response if the geometry is successfully retrieved from the database.
        """
        response = self.client.get(f'{self.base_url}geometry?id=a')
        self.assertEqual(response.status_code, 500)

    def test_geometry_with_nonexistent_id(self):
        """ 
            Test if the API returns a 404 response when the geometry is successfully retrieved
            with a nonexistent ID.

        Returns
        -------
            A 404 response if the geometry is successfully retrieved from the database.
        """ 
        response = self.client.get(f'{self.base_url}geometry?id=99')
        self.assertEqual(response.status_code, 404)

    # ---------------------------------------------------------------------------
    # TESTING PUT GEOMETRY
    # ---------------------------------------------------------------------------
    def test_put_valid_geometry(self):
        """ 
            Test if the API returns a 200 response when the geometry is successfully updated
            with a valid ID.

        Returns
        -------
            A 200 response if the geometry is successfully updated in the database.
        """
        self.test_post_valid_geometry()
        update_data = {
            "new_description": "Sample point"
        }
        response = self.client.put(f'{self.base_url}geometry?id=1', json=update_data)
        self.assertEqual(response.status_code, 200)

    def test_put_invalid_geometry(self):
        """ 
            Test if the API returns a 404 response when the geometry is successfully updated
            with an invalid ID.

        Returns
        -------
            A 404 response if the geometry is successfully updated in the database.
        """
        update_data = {
            "new_description": "Sample point"
        }
        response = self.client.put(f'{self.base_url}geometry?id=99', json=update_data)
        self.assertEqual(response.status_code, 404)

    # ---------------------------------------------------------------------------
    # TESTING DELETE GEOMETRY
    # ---------------------------------------------------------------------------
    def test_delete_valid_geometry(self):
        """
            Test if the API returns a 200 response when the geometry is successfully deleted
            with a valid ID.

        Returns
        -------
            A 200 response if the geometry is successfully deleted from the database.
        """
        self.test_post_valid_geometry()  # Ensure the resource exists before testing DELETE
        response = self.client.delete(f'{self.base_url}geometry?id=1')
        self.assertEqual(response.status_code, 200)

    def test_delete_invalid_geometry(self):
        """ 
            Test if the API returns a 404 response when the geometry is successfully deleted
            with an invalid ID.

        Returns
        -------
            A 404 response if the geometry is successfully deleted from the database.
        """
        response = self.client.delete(f'{self.base_url}geometry?id=99')
        self.assertEqual(response.status_code, 404)

    # ---------------------------------------------------------------------------
    # TESTING GET ADDRESS
    # ---------------------------------------------------------------------------

    def test_address_with_valid_placename(self):
        """ 
        Test if the API returns a 200 response when a valid placename is provided.

        Returns
        -------
        A 200 response if the address is successfully retrieved from the geocoding service.
        """
        payload = {'api_key': '66c3523802860766751470fxoc40658'}
        response = self.client.get(f'{self.base_url}adresses?placename=Statue+of+Liberty', json=payload)
        self.assertEqual(response.status_code, 200)

    def test_address_with_invalid_placename(self):
        """ 
        Test if the API returns a 404 response when an invalid placename is provided.

        Returns
        -------
        A 404 response if the address is not found in the geocoding service.
        """
        payload = {'api_key': '66c3523802860766751470fxoc40658'}
        response = self.client.get(f'{self.base_url}adresses?placename=Invalid+Placename', json=payload)
        self.assertEqual(response.status_code, 404)

    # ---------------------------------------------------------------------------
    # TESTING GET INFO BY COORDINATES
    # ---------------------------------------------------------------------------

    def test_info_by_coordinates(self):
        """
            Test if the API returns a 200 response when a valid coordinates are provided.

        Returns
        -------
            A 200 response if the info is successfully retrieved from the geocoding service.
        """
        payload = {'api_key': '66c3523802860766751470fxoc40658'}
        response = self.client.get(f'{self.base_url}coordinates?lat=40.7558017&lon=-73.9787414', json=payload)
        self.assertEqual(response.status_code, 200)

    def test_info_by_coordinates_invalid_coordinates(self):
        """
            Test if the API returns a 400 response when an invalid coordinates are provided.

        Returns
        -------
            A 400 response if the coordinates are invalid.
        """
        payload = {'api_key': '66c3523802860766751470fxoc40658'}
        response = self.client.get(f'{self.base_url}coordinates?lat=invalid&lon=invalid', json=payload)
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main(verbosity=2)
