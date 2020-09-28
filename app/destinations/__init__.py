#FROM https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xv-a-better-application-structure
from flask import Blueprint

#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
from app import db   # pragma: no cover
from app import users, schools, students, teachers, strengthes, weaknesses, destinations, goals, resources, models


dst = Blueprint('destinations', __name__, template_folder='templates')

from . import destinations