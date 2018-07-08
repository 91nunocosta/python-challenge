"""API definition."""
import os
import math
from urllib.parse import urlunparse, urlencode, ParseResult
from flask import Flask
from flask import request
from flask import jsonify
from autocomplete import Autocompleter 

def create_app(corpus_path=None):
    app = Flask(__name__)

    if corpus_path is None:
        corpus_path = os.getenv('CORPUS_PATH')

    with open(corpus_path) as corpus_file:
        words = (line.rstrip('\n') for line in corpus_file)
        autocompleter = Autocompleter(words)

    @app.route('/suggestions')
    def suggestions():
        prefix = request.args.get('q', '')
        suggestions = autocompleter.suggest(prefix)
        total = len(suggestions)
        limit = int(request.args.get('limit', total))
        offset = int(request.args.get('offset', 0))
        next_query = urlencode({
            'limit': limit,
            'offset': offset + limit
        })
        next_url = urlunparse(ParseResult(scheme='',netloc='', path='suggestions', params='', query=next_query, fragment=''))
        return jsonify(total=len(suggestions),
                       limit=limit,
                       offset=offset,
                       results=suggestions[offset:offset+limit],
                       next=next_url
                      )

    return app
