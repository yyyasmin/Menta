from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os

from flask_login import LoginManager
from config import basedir

from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD

from wtforms import *

app = Flask(__name__)
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

# from https://pythonhosted.org/Flask-Sijax/
import flask_sijax
#path = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')
app.config['SIJAX_STATIC_PATH'] = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')
app.config['SIJAX_JSON_URI'] = '/static/js/sijax/json2.js'
flask_sijax.Sijax(app)

# from https://pythonhosted.org/Flask-Sijax/



lm= LoginManager()
lm.init_app(app)
lm.login_view = 'login'

db = SQLAlchemy(app)

from flask_migrate import Migrate
migrate = Migrate(app, db)



#FROM https://github.com/HBalija/flask-blueprints/blob/master/app/site/__init__.py
from flask import Blueprint
#students = Blueprint('app/students', __name__, template_folder='app/templates' )
app.register_blueprint(students, url_prefix="/")

#FROM https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xv-a-better-application-structure
from app.students import std  
app.register_blueprint(std)


from app import users, schools, students, teachers, profile, strengthes, weaknesses, models



# for sending errors via mail
if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT), 'no-reply@' + MAIL_SERVER, ADMINS, 'menta failure', credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)
	
#enabling logging for debugging
'''
if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/menta.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('menta startup')
'''	

