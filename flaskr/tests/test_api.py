"""Test the suggestions API."""
from os import path
from unittest import TestCase
import json
from flaskr import create_app

class TestSuggestionsAPI(TestCase):
    
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['CORPUS_PATH'] = path.join(path.dirname(__file__), '../../test_files/190titles.csv')
        self.client = self.app.test_client()
    
    def test_can_get_suggestions(self):
        response = self.client.get('/suggestions?q=Fac')
        suggestions = json.loads(response.data)['results']
        expected_suggetions = [
            'Facebook',
            'Facebook Lite',
            'Facebook Pages Manager'
        ]
        self.assertListEqual(suggestions, expected_suggetions)
