#!/usr/bin/python3
"""create a route /status on the object app_views that returns a JSON."""
from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states/<state_id>cities', strict_slashes=False)
def all_City():
    """Retrieves the list of all State objects."""
    new_dict = []
    for state in storage.all('State').values():
        new_dict.append(state.to_dict())
    if len(new_dict) is not 0:
        city = new_dict[0].cities
        city = [c.to_dict() for c in city]
        return jsonify(city)
    else:
        abort(404)


@app_views.route('cities/<city_id>', strict_slashes=False,
                 methods=['GET'])
def get_city(city_id):
    """GET the list of all State objects."""
    try:
        city = jsonify(storage.get(City, city_id).to_dict())
        return city
    except:
        abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_City(city_id):
    """GET the list of all State objects."""
    state = storage.get(City, city_id)
    if state:
        state.delete(), storage.save()
        return {}
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_City(state_id):
    """POST the list of all State objects."""
    state = request.get_json()
    if type(state) is not dict:
        abort(400, {'Not a JSON'})
    elif 'name' not in state:
        abort(400, {'Missing name'})
    else:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        new_city = City()
        storage.new(new_city), storage.save()
        return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['PUT'])
def update_City(city_id):
    """PUT the list of all State objects."""
    update_state = request.get_json()
    if type(update_state) is not dict:
        abort(400, {'Not a JSON'})
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    else:
        for key, value in update_state.items():
            setattr(city, key, value)
        storage.save()
        return jsonify(city.to_dict())
