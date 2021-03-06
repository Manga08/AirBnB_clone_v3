#!/usr/bin/python3
"""Initialize app_views."""
from flask import Blueprint

app_views = Blueprint(
    'app_views',
    __name__,
    template_folder='templates',
    url_prefix="/api/v1")
