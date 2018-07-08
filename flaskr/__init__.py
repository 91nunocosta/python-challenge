"""API definition."""
import os
from flask import Flask
from flask import request
from flask import jsonify
from autocomplete import Autocompleter 

def create_app(corpus_path=None):
    app = Flask(__name__)

    if corpus_path is None:
        corpus_path = os.getenv('CORPUS_PATH')

    with open(corpus_path) as corpus_file:
        autocompleter = Autocompleter(word.rstrip('\n') for word in corpus_file)

    @app.route('/suggestions')
    def suggestions():
        prefix = request.args.get('q')
        suggestions = autocompleter.suggest(prefix)
        return jsonify(results=list(suggestions))

    return app
