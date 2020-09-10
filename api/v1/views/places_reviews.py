#!/usr/bin/python3
"""create a route /status on the object app_views that returns a JSON."""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def all_review(place_id):
    """Retrieves the list of all review objects."""
    new_dict = []
    if not storage.get(Place, place_id):
        abort(404)
    for review in storage.all('Review').values():
        if place_id == review.to_dict()['place_id']:
            new_dict.append(review.to_dict())
    return jsonify(new_dict)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET'])
def get_review(review_id):
    """GET the list of all review objects."""
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id):
    """GET the list of all review objects."""
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review), storage.save()
        return {}
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """POST the list of all review objects."""
    review = request.get_json()
    if not storage.get(Place, place_id):
        abort(404)
    if not review:
        abort(400, {'Not a JSON'})
    elif 'user_id' not in review:
        abort(400, {'Missing user_id'})
    elif not storage.get(User, review['user_id']):
        abort(404)
    elif 'text' not in review:
        abort(400, {'Missing text'})
    else:
        review['place_id'] = place_id
        new_review = Review(**review)
        storage.new(new_review)
        storage.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['PUT'])
def update_review(review_id):
    """PUT the list of all review objects."""
    update_review = request.get_json()
    if not update_review:
        abort(400, {'Not a JSON'})
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    else:
        for key, value in update_review.items():
            if key not in ['id', 'user_id', 'place_id', 'created_at',
                           'updated_at']:
                setattr(review, key, value)
        storage.save()
        return jsonify(review.to_dict())
