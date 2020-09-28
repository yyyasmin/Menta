from flask import render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, json
from flask_login import login_user, logout_user, current_user, login_required

from flask_login import LoginManager
from config import basedir
import config


from app import db
from app.forms import LoginForm, EditForm
from app.content_management import Content

from app.models import User, Student, Teacher, Profile, Strength, Weakness, School

from sqlalchemy import update

from app.users import usr
from app.students.students import student_home

#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
from flask import Blueprint
usr = Blueprint(
    'users', __name__,
    template_folder='templates'
) 
  
#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py



@usr.route('/signup', methods=['POST', 'GET'])   
def signup():

    if request.method == 'POST':
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        password_confirm=request.form['password_confirm']
        is_super_user = 'is_super_user' in request.form
        
        super_user_code=request.form['super_user_code']        
        if super_user_code != 'wearethechampions':
            flash("אין לך הרשאה לפתוח חשבון חדש. לפתיחת חשבון בבקשה תפנה לסמכות מתאימה.")
            return redirect(url_for('students.index'))
            
        if password == password_confirm:
            ##import pdb; pdb.set_trace()
            if User.query.filter(User.email==email).first() is None:
                print("BEFORE Enter to DDDDDBBBBBBBBBB")
                user = User(username, password, email, is_super_user)
                db.session.add(user)
                print("AFTER Enter to DDDDDBBBBBBBBBB")

                db.session.commit()				
                return redirect(url_for('students.student_home'))
            else:
                flash("There is already a user with this email.")
        else:
            flash("No match .")
        return render_template('student_signup.html')
    return render_template('student_signup.html')
		
	
@usr.route('/login', methods=['POST', 'GET'])
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
			return redirect(url_for('students.student_home'))
		else:
			flash("invalid username/password")
	return render_template('student_login.html')

						   						   
''' moved to models.py in User class						   						   
@login.user_loader  
def load_user(id):
	print("load user")
	return User.query.get(int(id))
@usr.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))	
'''	
	
##############  from 	http://stackoverflow.com/questions/9095923/using-flask-login-with-studentgresql
#@login_manager.user_loader
#def load_user(user_id):
#	user = User.query.get(user_id)
#	if user:
#	   return DbUser(user)
#   else:
#	   return None
##############  from 	http://stackoverflow.com/questions/9095923/using-flask-login-with-studentgresql

	
@usr.before_request
def before_request():
	print("bBBBBBBBBBBBBBBBBBBefore request")
	##import pdb; pdb.set_trace()
	#g.user = current_user
	#print("IN users in before_request g user is ")
	#print(g.user)
	

@usr.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    if user == None:
        flash('User %s not found.' % username)
        return redirect(url_for('students.index'))

    return render_template('user.html',
                            user=user,
                            )
                            
							
##############  from 	http://stackoverflow.com/questions/9095923/using-flask-login-with-studentgresql							
@usr.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You have logged out')
	return(redirect(url_for('users.login')))
##############  from 	http://stackoverflow.com/questions/9095923/using-flask-login-with-studentgresql

@usr.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404

@usr.errorhandler(500)
def internal_error(error):
	db.session.rollback()
	return render_template('500.html'), 500


@usr.route('/flash_err/')
def flash_err():
	TOPIC_DICT = Content()
	return render_template("flash_err.html", TOPIC_DICT = TOPIC_DICT)



@usr.route('/edit_users', methods=['GET', 'POST'])
@login_required
def edit_users():

    users = User.query.all()
    
    #DEBUG ONLY
    print("")
    for u in users:
        print("USER ", u.username)
        print("USER IS SUPER ", u.is_super_user)
        print("")
    #DEBUG ONLY
           
    users = User.query.all() 

    return render_template('edit_users.html', users=users)							


@usr.route('/user_update/<int:selected_user_id>', methods=['GET', 'POST'])
@login_required
def user_update(selected_user_id):

    user = User.query.filter(User.id == selected_user_id).first()
    if user == None:
        flash("Please select a Category to update first")
        return edit_users()
			
    if request.method == 'GET':
        #print("GET render update_user.html")
        return render_template('update_user.html', user=user)
        
    user.username = request.form.get('username')
    user.email = request.form.get('email')
        
    user.is_super_user = request.form.get('is_super_user') == 'on'
    
    print("")
    print("")
    print("")
    print("IN request.form.get('is_super_user') : ", request.form.get('is_super_user'))
    print("IN user_update user.is_super_user: ", user.is_super_user)
    print("")
    print("")
        
    db.session.commit()  
    db.session.refresh(user)
	
    return redirect(url_for('users.edit_users'))
	
    
	
		
@usr.route('/user_delete_for_good', methods=['GET', 'POST'])
@login_required
#Here author is user_id
def user_delete_for_good(user):
          
    print("")
    print ("delete for good selected user is " )
    print(user.username) 
    print("")
        
    db.session.delete(user)
    db.session.commit()
    flash ("User deleted Successfully")
            
    return redirect(url_for('users.edit_users')) 


@usr.route('/user_delete_for_good2/<int:selected_user_id>', methods=['GET', 'POST'])
#Here author is user_id
@login_required
def user_delete_for_good2(selected_user_id):

    #print ("SSSSSSSSSSSSSelected user is" )
    ################import pdb; pdb.set_trace()

    user = User.query.filter(User.id==selected_user_id).first()
    if user == None:
        flash("Please select a user to delete first ")
        return redirect(url_for('users.edit_users'))
        
    return user_delete_for_good(user)

