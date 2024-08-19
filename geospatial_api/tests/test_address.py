import sys
import os
import unittest
from pathlib import Path
from dotenv import load_dotenv
from geospatial_api.app import create_app
from geospatial_api.models.db import db

class TestAddressResource(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Set up the test client and app context. This method is called before any test case is run.
        """
        cls.base_url = "http://127.0.0.1:5000/"

        cls.app = create_app()
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()

        with cls.app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests."""
        with cls.app.app_context():
            db.drop_all()

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

    '''@patch('geospatial_api.resources.geocode.requests.get')
    def test_address_with_missing_parameters(self, mock_get):
        """ 
        Test if the API returns a 400 response when required parameters are missing.

        Returns
        -------
        A 400 response if required parameters are missing in the request.
        """
        response = self.client.get(f'{self.base_url}address', json={'api_key': 'dummy_key'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('message', response.json)
        self.assertEqual(response.json['message'], 'Please provide a placename')'''

if __name__ == "__main__":
    unittest.main(verbosity=2)
