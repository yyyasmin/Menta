#FROM microblog/app/__init__.py
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap

from config import Config

from wtforms import *

from flask_migrate import Migrate

db = SQLAlchemy()

migrate = Migrate(compare_type=True)
login = LoginManager()
login.login_view = 'users.login'
login.login_message = 'Please log in to access this page.'
mail = Mail()
bootstrap = Bootstrap()


#FROM https://github.com/miguelgrinberg/microblog/blob/v0.15/app/__init__.py	
def create_app(config_class=Config):
    app = Flask(__name__)
        
    app.config.from_object(config_class)
        
    db.init_app(app) 
    
    migrate.init_app(app, db)    
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)

    ### FROM https://github.com/mozilla/nunjucks/issues/296 ####
    app.jinja_env.add_extension('jinja2.ext.loopcontrols')
       
    from app.users.users import usr
    
    
    from app.schools.schools import scl
    from app.students.students import std
    from app.teachers.teachers import tchr
    
    from app.gts.gts import gt
    
    from app.weaknesses.weaknesses import wkns
    from app.strengthes.strengthes import strn
    from app.subjects.subjects import sbj

    from app.select.select import slct

    from app.destinations.destinations import dst
    from app.goals.goals import goal
    
    from app.accupations.accupations import acc
    from app.status.status import sts
    from app.tags.tags import tag
    from app.age_category.age_category import age
    from app.security.scrt import scrt

    from app.resources.resources import rsrc
    from app.documents.documents import doc

    from app.stars.stars import star1

    # register our blueprints
    app.register_blueprint(usr)
    
    app.register_blueprint(scl)
    app.register_blueprint(std)
    app.register_blueprint(tchr)
    
    app.register_blueprint(gt)
    
    app.register_blueprint(strn)
    app.register_blueprint(wkns)
    app.register_blueprint(sbj)
    app.register_blueprint(slct)

    app.register_blueprint(dst)
    app.register_blueprint(goal)
    
    app.register_blueprint(acc)   
    app.register_blueprint(sts)
    app.register_blueprint(tag)	        
    app.register_blueprint(age)    
    app.register_blueprint(scrt)
    
    app.register_blueprint(rsrc)
    app.register_blueprint(doc)

    app.register_blueprint(star1)

    return app

from app import models
from app.models import *
from app import *





