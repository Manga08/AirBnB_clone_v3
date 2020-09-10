#!/usr/bin/python3
"""create a route /status on the object app_views that returns a JSON."""
from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('states/<state_id>/cities', strict_slashes=False)
def all_City(state_id):
    """Retrieves the list of all cities objects."""
    new_dict = []
    if not storage.get(State, state_id):
        abort(404)
    for city in storage.all('City').values():
        if state_id == city.to_dict()['state_id']:
            new_dict.append(city.to_dict())
    return jsonify(new_dict)


@app_views.route('cities/<city_id>', strict_slashes=False,
                 methods=['GET'])
def get_city(city_id):
    """GET the list of all cities objects."""
    city = jsonify(storage.get(City, city_id).to_dict())
    try:
        return city
    except:
        abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_City(city_id):
    """GET the list of all cities objects."""
    cities = storage.get(City, city_id)
    if cities:
        storage.delete(cities), storage.save()
        return {}
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_City(state_id):
    """POST the list of all cities objects."""
    cities = request.get_json()
    if not storage.get(State, state_id):
        abort(404)
    if type(cities) is not dict:
        abort(400, {'Not a JSON'})
    elif 'name' not in cities:
        abort(400, {'Missing name'})
    else:
        cities['state_id'] = state_id
        new_City = City(**cities)
        storage.new(new_City)
        storage.save()
        return make_response(jsonify(new_City.to_dict()), 201)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['PUT'])
def update_City(city_id):
    """PUT the list of all cities objects."""
    update_cities = request.get_json()
    if type(update_cities) is not dict:
        abort(400, {'Not a JSON'})
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    else:
        for key, value in update_cities.items():
            setattr(city, key, value)
        storage.save()
        return jsonify(city.to_dict())
