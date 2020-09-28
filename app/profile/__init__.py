#FROM https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xv-a-better-application-structure
from flask import Blueprint

#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
from app import db   # pragma: no cover
from app import users, schools, students, teachers, profile, strengthes, weaknesses, destinations, goals, resources, models


prf = Blueprint('profile', __name__, template_folder='templates')

from . import profile