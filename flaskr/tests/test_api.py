"""Test the suggestions API."""
from os import path
from unittest import TestCase
import json
from flaskr import create_app

class TestSuggestionsAPI(TestCase):
    
    def setUp(self):
        self.corpus_path = path.join(path.dirname(__file__), '../../test_files/190titles.csv')
        self.app = create_app(corpus_path=self.corpus_path)
        self.app.config['TESTING'] = True
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

    def test_can_get_suggestions_for_empty_query(self):
        response = self.client.get('/suggestions')
        suggestions = json.loads(response.data)['results']
        with open(self.corpus_path) as corpus_file:
            expected_suggetions = set(line.rstrip('\n') for line in corpus_file)
        self.assertEqual(set(suggestions), expected_suggetions )
