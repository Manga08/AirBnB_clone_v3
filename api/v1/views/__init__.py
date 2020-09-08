#!/usr/bin/python3
"""Initialize app_views."""
from flask import Blueprint
from api.v1.views.index import *
app_views = Blueprint('app_views', __name__, template_folder='templates')
