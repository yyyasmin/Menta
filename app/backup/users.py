from flask import render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, json
from flask_login import login_user, logout_user, current_user, login_required
#from flask_login import login_manager

from flask_login import LoginManager
from config import basedir
import config

from app import app, db
from app import lm
from .forms import LoginForm

#from .models import User, Student, Team_member, Profile, Strength, Weaknesse
from .models import Team_member
from .forms import LoginForm, EditForm

from sqlalchemy import update

from .content_management import Content


@app.route('/student_home' )
def student_home():
	print("in student_home")
	return render_template('student_home.html')
	
	
@app.route('/signup', methods=['POST', 'GET'])   
def signup():
	if request.method == 'POST':
		username=request.form['username']
		email=request.form['email']
		password=request.form['password']
		password_confirm=request.form['password_confirm']
		if password == password_confirm:
			import pdb; pdb.set_trace()
			if User.query.filter(User.email==email).first() is None:
				print("BEFORE Enter to DDDDDBBBBBBBBBB")
				user= User(username, password, email)
				db.session.add(user)
				print("AFTER Enter to DDDDDBBBBBBBBBB")

				db.session.commit()				
				return redirect(url_for('student_home'))
			else:
				flash("There is already a user with this email.")
		else:
			flash("No match .")
		return render_template('student_signup.html')
	return render_template('student_signup.html')
		
	
@app.route('/login', methods=['POST', 'GET'])
def login():
	if request.method == 'POST':
		email=request.form['email']
		password=request.form['password']
		user=User.query.filter_by(email=email).first()
		if user == None:
			flash("invalid username/password")
			return render_template('student_login.html')
		userToCheck = User.query.filter(User.email==email).first()
		
		if userToCheck.password == password:
			login_user(user)
			return redirect(url_for('student_home'))
		else:
			flash("invalid username/password")
	return render_template('student_login.html')

						   						   
@lm.user_loader  
def load_user(id):
	print("load user")
	return User.query.get(int(id))
	
	
##############  from 	http://stackoverflow.com/questions/9095923/using-flask-login-with-studentgresql
#@login_manager.user_loader
#def load_user(user_id):
#	user = User.query.get(user_id)
#	if user:
#	   return DbUser(user)
#   else:
#	   return None
##############  from 	http://stackoverflow.com/questions/9095923/using-flask-login-with-studentgresql

	
@app.before_request
def before_request():
	print("bBBBBBBBBBBBBBBBBBBefore request")
	g.user = current_user
	

@app.route('/user/<username>')
#@login_required
def user(username):
	user = User.query.filter_by(username=username).first()
	if user == None:
		flash('User %s not found.' % username)
		return redirect(url_for('index'))

	return render_template('user.html',
							user=user,
							)
							
							
##############  from 	http://stackoverflow.com/questions/9095923/using-flask-login-with-studentgresql							
@app.route('/Dblogout')
@login_required
def logout():
	logout_user()
	flash('You have logged out')
	return(redirect(url_for('login')))
##############  from 	http://stackoverflow.com/questions/9095923/using-flask-login-with-studentgresql

@app.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
	db.session.rollback()
	return render_template('500.html'), 500


@app.route('/flash_err/')
def flash_err():
	TOPIC_DICT = Content()
	return render_template("flash_err.html", TOPIC_DICT = TOPIC_DICT)


