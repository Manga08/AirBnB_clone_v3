#!/usr/bin/python3
"""create a route /status on the object app_views that returns a JSON."""
from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def all_places(city_id):
    """Retrieves the list of all place objects."""
    new_dict = []
    if not storage.get(City, city_id):
        abort(404)
    for plc in storage.all('Place').values():
        if city_id == plc.to_dict()['city_id']:
            new_dict.append(plc.to_dict())
    return jsonify(new_dict)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET'])
def get_place(place_id):
    """GET the list of all place objects."""
    try:
        plc = jsonify(storage.get(Place, place_id).to_dict())
        return plc
    except BaseException:
        abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id):
    """GET the list of all place objects."""
    plc = storage.get(Place, place_id)
    if plc:
        plc.delete(), storage.save()
        return {}
    else:
        abort(404)


@app_views.route('cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """POST the list of all place objects."""
    plc = request.get_json()
    if not storage.get(City, city_id):
        abort(404)
    if type(plc) is not dict:
        abort(400, {'Not a JSON'})
    elif 'user_id' not in plc:
        abort(400, {'Missing user_id'})
    elif 'name' not in plc:
        abort(400, {'Missing name'})
    elif not storage.get(User, plc['user_id']):
        abort(404)
    else:
        plc['city_id'] = city_id
        new_plc = Place(**plc)
        storage.new(new_plc)
        storage.save()
        return make_response(jsonify(new_plc.to_dict()), 201)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['PUT'])
def update_place(place_id):
    """PUT the list of all place objects."""
    update_plc = request.get_json()
    if type(update_plc) is not dict:
        abort(400, {'Not a JSON'})
    plc = storage.get(Place, place_id)
    if not plc:
        abort(404)
    else:
        for key, value in update_plc.items():
            if key not in ['id', 'user_id', 'city_id', 'created_at',
                           'updated_at']:
                setattr(plc, key, value)
        storage.save()
        return jsonify(plc.to_dict())
