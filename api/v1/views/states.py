#!/usr/bin/python3
"""create a route /status on the object app_views that returns a JSON."""
from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
def all_States():
    """Retrieves the list of all State objects."""
    new_dict = []
    for state in storage.all('State').values():
        new_dict.append(state.to_dict())
    return jsonify(new_dict)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['GET'])
def get_state(state_id):
    """GET the list of all State objects."""
    try:
        state = jsonify(storage.get(State, state_id).to_dict())
        return state
    except:
        abort(404)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    """GET the list of all State objects."""
    state = storage.get(State, state_id)
    if state:
        state.delete(), storage.save()
        return {}
    else:
        abort(404)


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def create_state():
    """POST the list of all State objects."""
    state = request.get_json()
    if type(state) is not dict:
        abort(400, {'Not a JSON'})
    elif 'name' not in state:
        abort(400, {'Missing name'})
    else:
        new_state = State(**state)
        storage.new(new_state)
        storage.save()
        return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['PUT'])
def update_state(state_id):
    """PUT the list of all State objects."""
    update_state = request.get_json()
    if type(update_state) is not dict:
        abort(400, {'Not a JSON'})
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    else:
        for key, value in update_state.items():
            setattr(state, key, value)
        storage.save()
        return jsonify(state.to_dict())
