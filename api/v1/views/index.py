#!/usr/bin/python3
"""create a route /status on the object app_views that returns a JSON."""
from flask import Flask
from api.v1.views import app_views
from models import storage


@app_views.route('/api/v1/status', strict_slashes=False)
def status():
    """Return a JSON."""
    return {"status": "OK"}


@app_views.route('/api/v1/stats', strict_slashes=False)
def stats():
    """Endpoint that retrieves the number of each objects by type."""
    return {"amenities": storage.count('Amenity'),
            "cities": storage.count('City'),
            "places": storage.count('Place'),
            "reviews": storage.count('Review'),
            "states": storage.count('State'),
            "users": storage.count('User')}