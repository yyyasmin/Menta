#!flask/bin/python
import imp
from migrate.versioning import api
print('New migration 111111111' )

print('New migration2222222222222s ' )

########## usually called in run.py ################

from app import create_app, db

from app.models import User, Student, Teacher, Profile, Strength, Weakness
from app.models import General_txt, Destination, Goal, Todo
from app.models import Profile, Strength, Weakness, Subject
from app.models import  Role, Std_general_txt
from app.models import  Tag, Accupation, Status, Scrt, Resource, Document, Ufile

app = create_app()  
########## usually called in run.py ################

SQLALCHEMY_DATABASE_URI = app.config.get('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_MIGRATE_REPO = app.config.get('SQLALCHEMY_MIGRATE_REPO')

print ("In MMMMMMMMMMMMMMMigrate: SQLALCHEMY_DATABASE_URI  SQLALCHEMY_MIGRATE_REPO", SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
'''
#DEBUG
t = api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, 103)
print('New migration 555555555555555 v=:' + str(v) +  't=:' + str(t))
#DEBUG
'''

migration = SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (v+1))
print('New migration 66666666666666666 ' + migration)

tmp_module = imp.new_module('old_model')
print('New migration 77777777777777777777 ' + migration)

old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print('New migration 888888888888888888 ' + migration)

exec(old_model, tmp_module.__dict__)
print('New migration 999999999999999999 ' + migration + "tmp_modle dict" + str(tmp_module.__dict__))
import pdb; pdb.set_trace()
script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, tmp_module.meta, db.metadata)
print('New migration saved as ' + migration)

open(migration, "wt").write(script)
print('New migration 1010101010 ' + migration)

api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print('New migration 111111111111111 ' + migration)

v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print('New migration saved as ' + migration)
print('Current database version: ' + str(v))