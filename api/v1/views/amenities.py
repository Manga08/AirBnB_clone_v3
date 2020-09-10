#!/usr/bin/python3
"""create a route /status on the object app_views that returns a JSON."""
from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False)
def all_amenitys():
    """Retrieves the list of all amenity objects."""
    new_dict = []
    for amnty in storage.all('Amenity').values():
        new_dict.append(amnty.to_dict())
    return jsonify(new_dict)


@app_views.route('amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET'])
def get_amenity(amenity_id):
    """GET the list of all amenity objects."""
    try:
        amnty = jsonify(storage.get(Amenity, amenity_id).to_dict())
        return amnty
    except BaseException:
        abort(404)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id):
    """GET the list of all amenity objects."""
    amnty = storage.get(Amenity, amenity_id)
    if amnty:
        amnty.delete(), storage.save()
        return {}
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """POST the list of all amenity objects."""
    amenity = request.get_json()
    if type(amenity) is not dict:
        abort(400, {'Not a JSON'})
    elif 'name' not in amenity:
        abort(400, {'Missing name'})
    else:
        new_amnty = Amenity(**amenity)
        storage.new(new_amnty)
        storage.save()
        return make_response(jsonify(new_amnty.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def update_amenity(amenity_id):
    """PUT the list of all amenity objects."""
    update_amnty = request.get_json()
    if type(update_amnty) is not dict:
        abort(400, {'Not a JSON'})
    amnty = storage.get(Amenity, amenity_id)
    if not amnty:
        abort(404)
    else:
        for key, value in update_amnty.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amnty, key, value)
        storage.save()
        return jsonify(amnty.to_dict())
