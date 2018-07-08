"""Test the suggestions API."""
from os import path
from unittest import TestCase
import json
from urllib.parse import urlparse, parse_qs
from flaskr import create_app

class TestSuggestionsAPI(TestCase):
    """Test GET /suggestions requests."""
    
    def setUp(self):
        """Setsup the a test client for the API."""
        self.corpus_path = path.join(path.dirname(__file__), '../../test_files/190titles.csv')
        self.app = create_app(corpus_path=self.corpus_path)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_can_get_suggestions(self):
        """Test can get all suggestions for a given prefix."""
        response = self.client.get('/suggestions?q=Fac')
        suggestions = json.loads(response.data)['results']
        expected_suggetions = [
            'Facebook',
            'Facebook Lite',
            'Facebook Pages Manager'
        ]
        self.assertListEqual(suggestions, expected_suggetions)

    def test_can_get_suggestions_for_empty_query(self):
        """Test can get all suggestions when no prefix is specified."""
        response = self.client.get('/suggestions')
        suggestions = json.loads(response.data)['results']
        with open(self.corpus_path) as corpus_file:
            expected_suggetions = set(line.rstrip('\n') for line in corpus_file)
        self.assertEqual(set(suggestions), expected_suggetions )
    
    def test_can_paginate_suggestions(self):
        """Test can iterate over suggestion results pages."""
        next_page = '/suggestions?limit=10'
        for page in range(3):
            response = self.client.get(next_page)
            payload = json.loads(response.data)
            self.assertEqual(payload['total'], 187)
            self.assertEqual(payload['limit'], 10)
            self.assertEqual(len(payload['results']), 10)
            self.assertEqual(payload['offset'], 10*page)
            next_page = payload['next']
            query_parameters = parse_qs(urlparse(next_page).query)
            self.assertDictEqual(query_parameters, {
                'limit': ['10'],
                'offset': [str(10*(page+1))]
            })
    
    def test_can_get_suggestions_page_after_all_results(self):
        """Test can get suggestions with an offset which is greater than the number of results."""
        response = self.client.get('/suggestions?offset=1000')
        payload = json.loads(response.data)
        self.assertEqual(len(payload['results']), 0)

    def test_last_suggestions_page_hasnt_next(self):
        """Test that the last page in the suggests results doesn't has a next link."""
        response = self.client.get('/suggestions?limit=10&offset=177')
        payload = json.loads(response.data)
        self.assertIsNone(payload.get('next', None))

    def test_can_handle_invalid_limit(self):
        """Test responses with HTTP 400 Bad Request when the requested limit is invalid."""
        response = self.client.get('suggestions?limit=a')
        self.assertEqual(response.status_code, 400)
    
    def test_can_handle_invalid_offset(self):
        """Test responses with HTTP 400 Bad Request when the requested offset is invalid."""
        response = self.client.get('suggestions?offset=b')
        self.assertEqual(response.status_code, 400)