#!/usr/bin/python3
"""create a route /status on the object app_views that returns a JSON."""
from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False)
def all_States():
    """Retrieves the list of all State objects."""
    new_dict = []
    for amnty in storage.all(Amenity).values():
        new_dict.append(amnty.to_dict())
    return jsonify(new_dict)


@app_views.route('amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET'])
def get_state(amenity_id):
    """GET the list of all State objects."""
    try:
        amnty = jsonify(storage.get(Amenity, amenity_id).to_dict())
        return amnty
    except:
        abort(404)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_state(amenity_id):
    """GET the list of all State objects."""
    amnty = storage.get(Amenity, amenity_id)
    if amnty:
        amnty.delete(), storage.save()
        return {}
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_state():
    """POST the list of all State objects."""
    state = request.get_json()
    if type(state) is not dict:
        abort(400, {'Not a JSON'})
    elif 'name' not in state:
        abort(400, {'Missing name'})
    else:
        amnty = Amenity()
        storage.new(amnty)
        storage.save()
        return make_response(jsonify(amnty.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def update_state(amenity_id):
    """PUT the list of all State objects."""
    update_amnty = request.get_json()
    if type(update_amnty) is not dict:
        abort(400, {'Not a JSON'})
    amnty = storage.get(Amenity, amenity_id)
    if not amnty:
        abort(404)
    else:
        for key, value in update_amnty.items():
            setattr(amnty, key, value)
        storage.save()
        return jsonify(amnty.to_dict())
