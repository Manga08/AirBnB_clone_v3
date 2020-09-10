#!/usr/bin/python3
"""create a route /status on the object app_views that returns a JSON."""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', strict_slashes=False)
def all_amenities(place_id):
    """Retrieves the list of all amenities objects."""
    plc = storage.get(Place, place_id)
    new_dict = []
    if not plc:
        abort(404)
    for amenity in plc.amenities:
            new_dict.append(amenity.to_dict())
    return jsonify(new_dict)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_amenities(place_id, amenity_id):
    """GET the list of all review objects."""
    plc = storage.get(Place, place_id)
    if not plc:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    elif amenity not in plc.amenities:
        abort(404)
    else:
        plc.amenities.remove(amenity)
        storage.save()
        return {}


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def create_amenities(place_id, amenity_id):
    """POST the list of all amenities objects."""
    plc = storage.get(Place, place_id)
    if not plc:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    elif amenity in plc.amenities:
        return jsonify(amenity.to_dict())
    else:
        plc.amenities.append(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201
