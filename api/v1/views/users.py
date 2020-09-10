#!/usr/bin/python3
"""create a route /status on the object app_views that returns a JSON."""
from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False)
def all_Users():
    """Retrieves the list of all user objects."""
    new_dict = []
    for usr in storage.all('User').values():
        new_dict.append(usr.to_dict())
    return jsonify(new_dict)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['GET'])
def get_user(user_id):
    """GET the list of all user objects."""
    usr = storage.get(User, user_id)
    if usr:
        return jsonify(usr.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_user(user_id):
    """GET the list of all user objects."""
    usr = storage.get(User, user_id)
    if usr:
        usr.delete(), storage.save()
        return {}
    else:
        abort(404)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def create_user():
    """POST the list of all user objects."""
    usr = request.get_json()
    if not usr:
        abort(400, {'Not a JSON'})
    elif 'email' not in usr:
        abort(400, {'Missing email'})
    elif 'password' not in usr:
        abort(400, {'Missing password'})
    else:
        new_usr = User(**usr)
        storage.new(new_usr)
        storage.save()
        return make_response(jsonify(usr.to_dict()), 201)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['PUT'])
def update_user(user_id):
    """PUT the list of all user objects."""
    update_usr = request.get_json()
    if not update_usr:
        abort(400, {'Not a JSON'})
    usr = storage.get(User, user_id)
    if not usr:
        abort(404)
    else:
        for key, value in update_usr.items():
            setattr(usr, key, value)
        storage.save()
        return jsonify(usr.to_dict())
