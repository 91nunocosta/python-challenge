"""API definition."""
from flask import Flask
from flask import jsonify

def create_app():
    app = Flask(__name__)

    @app.route('/suggestions')
    def suggestions():
        return jsonify(results=[])

    return app
