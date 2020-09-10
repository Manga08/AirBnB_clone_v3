#!/usr/bin/python3
"""create a route /status on the object app_views that returns a JSON."""
from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.user import User
from models.city import City
from models.place import Place


@app_views.route('/api/v1/cities/<city_id>/places', strict_slashes=False)
def all_places(city_id):
    """Retrieves the list of all State objects."""
    new_dict = list(storage.get(City, city_id))
    if new_dict is not None
        for plc in new_dict:
            new_dict.append(plc.to_dict())
        return jsonify(new_dict)
    return abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET'])
def get_state(place_id):
    """GET the list of all State objects."""
    try:
        plc = jsonify(storage.get(Place, place_id).to_dict())
        return plc
    except:
        abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_state(place_id):
    """GET the list of all State objects."""
    plc = storage.get(Place, place_id)
    if plc:
        plc.delete(), storage.save()
        return {}
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_state(city_id):
    """POST the list of all State objects."""
    plc = request.get_json()
    if type(plc) is not dict:
        abort(400, {'Not a JSON'})
    elif 'user_id' not in plc:
        abort(400, {'Missing user_id'})
    elif 'name' not in plc:
        abort(400, {'Missing name'})
    else:
        usr_obj = storage.get('User', plc['user_id'])
        if usr_obj is None:
            abort(404)
        new_plc = Place()
        storage.new(new_plc)
        storage.save()
        return make_response(jsonify(new_plc.to_dict()), 201)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['PUT'])
def update_state(place_id):
    """PUT the list of all State objects."""
    update_plc = request.get_json()
    if type(update_plc) is not dict:
        abort(400, {'Not a JSON'})
    plc = storage.get(Place, place_id)
    if not plc:
        abort(404)
    else:
        for key, value in update_plc.items():
            setattr(plc, key, value)
        storage.save()
        return jsonify(plc.to_dict())
