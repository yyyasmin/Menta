from flask import render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from flask import render_template, flash, redirect, session, url_for, request, jsonify, json
from flask_login import login_user, logout_user, current_user, login_required
#from flask_login import login_manager

from flask_login import LoginManager
from config import basedir
import config

from app import current_app, db
from app.forms import LoginForm

from app.models import User, Student, Teacher, Profile, Strength, Weakness, Tag, Destination, Goal, Accupation
from app.forms import LoginForm, EditForm

from sqlalchemy import update

from app.content_management import Content

#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
from flask import Blueprint
strn = Blueprint(
    'strengthes', __name__,
    template_folder='templates'
)   

#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
from app.select.select import student_select2, profile_select2, strength_select2, strength_select2, accupation_select2, goal_select2, resource_select2
from app import *
from datetime import datetime



@strn.route('/strengthes_by_profile', methods=['POST', 'GET'])
@login_required
def strengthes_by_profile():
	
    student = Student.query.filter(Student.selected==True).first()
    if student == None:
        flash("Please select a student first ")
        return redirect(url_for('index'))
	
    profile = Profile.query.filter(Profile.selected==True).first()
    print("in strengthes_by_profile profile selected is")
    print(profile.title)
    if profile == None:
        flash("Please select an profile first ")
        return redirect(url_for('profile_select'))
	
    ##import pdb; pdb.set_trace()
    strengthes = Strength.query.join(Profile.strengthes).filter(Profile.id==profile.id)
    return render_template('show_profile_strengthes2.html',
                            student=student,
                            profile=profile,
                            strengthes=strengthes
							)

@strn.route('/strengthes_by_profile2/<int:selected_profile_id>', methods=['POST', 'GET'])
@login_required
def strengthes_by_profile2(selected_profile_id):
    print("IIn PRRRRRRRRRRRROs AAAAAAAAAAAAAProfile 22222222222222")
    print(selected_profile_id)
    profile_select2(selected_profile_id)
    return redirect(url_for('strengthes_by_profile'))						

@strn.route('/edit_strengthes', methods=['GET', 'POST'])
@login_required
def edit_strengthes():
    student = Student.query.filter(Student.selected==True).first()
    if student == None:
        flash("Please select a student first ")
        return redirect(url_for('index'))
	
    profile = Profile.query.filter(Profile.selected==True).first()
    print("in strengthes_by_profile profile selected is")
    print(profile.title)
    if profile == None:
        flash("Please select an profile first ")
        return redirect(url_for('profile_select'))
	
    ##import pdb; pdb.set_trace()
    strengthes = Strength.query.join(Profile.strengthes).filter(Profile.id==profile.id)
    return render_template('edit_strengthes.html',
                            student=student,
                            profile=profile,
                            strengthes=strengthes
							)

	
@strn.route('/strength_add', methods=['GET', 'POST'])
def strength_add():

	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('index'))
		
	profile = Profile.query.filter(Profile.selected==True).first()

	if profile == None:
		flash("Please select an profile first ")
		return redirect(url_for('profile_select'))
	print(profile.title)      
	#print request

	if request.method == 'GET':
		return render_template('strength_to_profile_add.html', student=student, profile=profile)
	###############################################################################		

		   
	#get data from form and insert to strengthgress db
	title = request.form.get('title')
	body = request.form.get('description')

	##import pdb; pdb.set_trace() 	
	author_id = current_user._get_current_object().id
	strength = Strength(title, body, author_id)

	profile.strengthes.append(strength)	

	db.session.add(strength)    
	db.session.commit()  
	db.session.refresh(strength)

	url = url_for('students.edit_students_profile')
	return redirect(url)   
	
#update selected strength
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@strn.route('/strength_update/<int:selected_strength_id>', methods=['GET', 'POST'])
def strength_update(selected_strength_id):

    strength_select2(selected_strength_id)
		
    strength = Strength.query.get_or_404(selected_strength_id)
    print("In PPPPPPPPPPPPstrength UUUUUUUUUUUUUUUUUUUUUUpdate")
    print(selected_strength_id, strength.id, strength.title)
	
    if request.method == 'GET':
        print("GET render update_strength.html")
        return render_template('update_strength.html', strength=strength)
		
    #get data from form and insert to strengthgress db
    ##import pdb; pdb.set_trace() 	
    strength.title = request.form.get('title')	
    strength.body = request.form.get('body')
    
    db.session.commit()  
    db.session.refresh(strength)
	
    return redirect(url_for('students.edit_students_profile'))
	
		
@strn.route('/strength_delete_for_good', methods=['GET', 'POST'])
#Here author is user_id
def strength_delete_for_good():
	  
	user = User.query.get_or_404(current_user.id)
	author_id = user.id

	strength = Strength.query.filter(Strength.selected==True).first()
	if strength == None:
		flash("Please select a strength to delete first ")
		return redirect(url_for('select.strength_select'))
			
	print ("delete selected strength is " )
	print(strength.title)      

	db.session.delete(strength) 

	db.session.commit()  

	return redirect(url_for('students.edit_students_profile')) 
		
#delete from index strengthes list
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@strn.route('/strength_delete_for_good2/<int:selected_strength_id>', methods=['GET', 'POST'])
#Here author is user_id
def strength_delete_for_good2(selected_strength_id):

	print ("SSSSSSSSSSSSSelected strength is" )
	strength_select2(selected_strength_id)
	return redirect(url_for('strengthes.strength_delete_for_good')) 	

