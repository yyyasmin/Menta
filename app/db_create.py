#!flask/bin/python
from migrate.versioning import api
#from config import SQLALCHEMY_MIGRATE_REPO
#from config import SQLALCHEMY_DATABASE_URI
import config
#from flask import current_app
#from app import db
import os.path

########## usually called in run.py ################
from app import create_app, db
from app.models import User, Student, Teacher, Profile, Strength, Weaknesse, Role
app = create_app()  
########## usually called in run.py ################
import pdb; pdb.set_trace()
SQLALCHEMY_DATABASE_URI = app.config.get('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_MIGRATE_REPO = app.config.get('SQLALCHEMY_MIGRATE_REPO')

#do everything from https://www.mbeckler.org/blog/?p=218
from sqlalchemy import *
from sqlalchemy.schema import *
from sqlalchemy.engine import reflection
#from flask.ext.sqlalchemy import SQLAlchemy

#from https://github.com/numpy/numpy/issues/7556
import collections
import numpy

#FROM http://flask-sqlalchemy.pocoo.org/2.3/contexts/
with.app_context():
#FROM http://flask-sqlalchemy.pocoo.org/2.3/contexts/

	conn=db.engine.connect()

	# the transaction only applies if the DB supports
	# transactional DDL, i.e. Postgresql, MS SQL Server
	trans = conn.begin()

	from sqlalchemy.engine import reflection
	inspector = reflection.Inspector.from_engine(db.engine)

	# gather all data first before dropping anything.
	# some DBs lock after things have been dropped in 
	# a transaction.
	metadata = MetaData()

	tbs = []
	all_fks = []

	for table_name in inspector.get_table_names():
		fks = []
		for fk in inspector.get_foreign_keys(table_name):
			if not fk['name']:
				continue
			fks.append(
				ForeignKeyConstraint((),(),name=fk['name'])
				)
		t = Table(table_name,metadata,*fks)
		tbs.append(t)
		all_fks.extend(fks)

	for fkc in all_fks:
		conn.execute(DropConstraint(fkc))

	for table in tbs:
		conn.execute(DropTable(table))

	trans.commit()
	#do everything from https://www.mbeckler.org/blog/?p=218


db.reflect()
db.drop_all()
db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))