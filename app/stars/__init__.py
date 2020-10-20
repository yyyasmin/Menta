#FROM https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xv-a-better-application-structure
from flask import Blueprint

#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
from app import db   # pragma: no cover
from app import users, stars, students, teachers, strengthes, weaknesses, models


star1 = Blueprint('stars', __name__, template_folder='templates')

from . import stars