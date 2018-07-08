"""API definition."""
import os
import math
from urllib.parse import urlunparse, urlencode, ParseResult
from flask import Flask
from flask import request
from flask import Response
from flask import jsonify
from flask import abort
from autocomplete import Autocompleter 

def create_app(corpus_path=None):
    """Flask Application Factory.
    
    Optional Arguments:
    corpus_path: the path for the corpus file, which sould be a list with a word by line.
    """
    app = Flask(__name__)

    if corpus_path is None:
        corpus_path = os.getenv('CORPUS_PATH')

    with open(corpus_path) as corpus_file:
        words = (line.rstrip('\n') for line in corpus_file)
        autocompleter = Autocompleter(words)

    @app.route('/suggestions')
    def suggestions():
        """GET /suggestions end-point.
        
        Accepted Query Parameters:
        q: the prefix. 
        limit: the number of reslts by page.
        offset: the position of the first result in the list of all suggestions.
        """
        prefix = request.args.get('q', '')
        suggestions = autocompleter.suggest(prefix)
        total = len(suggestions)
        try:
            limit = int(request.args.get('limit', total))
            offset = int(request.args.get('offset', 0))
        except ValueError:
            abort(400)
        response = {
            'total': len(suggestions),
            'limit': limit,
            'offset': offset,
            'results': suggestions[offset:offset+limit]
        }
        if offset < total - limit:
            next_query = urlencode({
                'limit': limit,
                'offset': offset + limit
            })
            next_url = urlunparse(ParseResult(scheme='',
                                              netloc='', 
                                              path='suggestions', 
                                              params='', 
                                              query=next_query, 
                                              fragment=''))
            response['next'] = next_url
        return jsonify(response)

    return app
