from flask import render_template, flash, redirect
from flask import render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, json
from flask_login import login_user, logout_user, current_user, login_required
#from flask_login import login_manager

from flask_login import LoginManager
from config import basedir
import config

from app import  db

from app.forms import LoginForm, EditForm



from app.forms import LoginForm, EditForm

from app.templates import *
### FROM https://gist.github.com/astrolox/445e84068d12ed9fa28f277241edf57b

from sqlalchemy import update

from app.content_management import Content

from sqlalchemy import text # for execute SQL raw SELECT ...

from datetime import date

import functools
import logging
import time

from flask import request
from flask_socketio import emit, ConnectionRefusedError, disconnect

from .auth import is_logged_in
from .io_blueprint import IOBlueprint

logger = logging.getLogger(__name__)
bp = IOBlueprint('events', __name__)



@bp.on('connect')
def connect():
    emit('flash', 'Welcome ' + request.remote_user)  # context aware emit


@bp.on('echo')
@login_required
def on_alive(data):
    emit('echo', data)  # context aware emit


@bp.on('broadcast')
@login_required
def on_broadcast(data):
    bp.emit('broadcast', data)  # bp.emit same as socketio.emit