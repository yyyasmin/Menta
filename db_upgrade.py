#!flask/bin/python
from migrate.versioning import api

########## usually called in run.py ################
from app import create_app, db
from app.models import User, Student, Teacher, Profile, Strength, Weakness, Role
app = create_app()  
########## usually called in run.py ################

SQLALCHEMY_DATABASE_URI = app.config.get('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_MIGRATE_REPO = app.config.get('SQLALCHEMY_MIGRATE_REPO')

api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print('Current database version: ' + str(v))