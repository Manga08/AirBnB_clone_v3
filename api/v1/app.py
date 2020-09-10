#!/usr/bin/python3
"""Start a Flask web application."""
from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from os import getenv
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def remove_session(response_or_exc):
    """Remove the current SQLAlchemy session."""
    storage.close()


@app.errorhandler(404)
def not_found(self):
    """Handler for 404 error that returns a JSON-formatted."""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    HBNB_API_PORT = getenv('HBNB_API_PORT')
    if not HBNB_API_HOST:
        HBNB_API_HOST = '0.0.0.0'
    if not HBNB_API_PORT:
        HBNB_API_PORT = 5000
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True, debug=True)
