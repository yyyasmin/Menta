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

from app.models import User, Student, Teacher, Profile, Subject, Weakness, Tag, Destination, Goal, Accupation
from app.forms import LoginForm, EditForm

from sqlalchemy import update

from app.content_management import Content

#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
from flask import Blueprint
sbj = Blueprint(
    'subjects', __name__,
    template_folder='templates'
)   

#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
from app.select.select import student_select2, profile_select2, subject_select2, subject_select2, accupation_select2, goal_select2, resource_select2
from app import *
from datetime import datetime



@sbj.route('/subjectes_by_profile', methods=['POST', 'GET'])
@login_required
def subjectes_by_profile():
	
    student = Student.query.filter(Student.selected==True).first()
    if student == None:
        flash("Please select a student first ")
        return redirect(url_for('index'))
	
    profile = Profile.query.filter(Profile.selected==True).first()
    print("in subjectes_by_profile profile selected is")
    print(profile.title)
    if profile == None:
        flash("Please select an profile first ")
        return redirect(url_for('profile_select'))
	
    ##import pdb; pdb.set_trace()
    subjectes = Subject.query.join(Profile.subjects).filter(Profile.id==profile.id)
    return render_template('show_profile_subjectes2.html',
                            student=student,
                            profile=profile,
                            subjectes=subjectes
							)

@sbj.route('/subjectes_by_profile2/<int:selected_profile_id>', methods=['POST', 'GET'])
@login_required
def subjectes_by_profile2(selected_profile_id):
    print("IIn PRRRRRRRRRRRROs AAAAAAAAAAAAAProfile 22222222222222")
    print(selected_profile_id)
    profile_select2(selected_profile_id)
    return redirect(url_for('subjectes_by_profile'))						

@sbj.route('/edit_subjectes', methods=['GET', 'POST'])
@login_required
def edit_subjectes():
    student = Student.query.filter(Student.selected==True).first()
    if student == None:
        flash("Please select a student first ")
        return redirect(url_for('index'))
	
    profile = Profile.query.filter(Profile.selected==True).first()
    print("in subjectes_by_profile profile selected is")
    print(profile.title)
    if profile == None:
        flash("Please select an profile first ")
        return redirect(url_for('profile_select'))

    all_subjects = Subject.query.all()
    ##import pdb; pdb.set_trace()
    subjectes = Subject.query.join(Profile.subjects).filter(Profile.id==profile.id)

    return render_template('add_subject_to_std_profile.html',
                            student=student,
                            profile=profile,
                            subjectes=all_subjects
							)

	
@sbj.route('/subject_add', methods=['GET', 'POST'])
def subject_add():

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
		return render_template('subject_to_profile_add.html', student=student, profile=profile)
	###############################################################################		

		   
	#get data from form and insert to subjectgress db
	title = request.form.get('title')
	body = request.form.get('description')

	##import pdb; pdb.set_trace() 	
	author_id = current_user._get_current_object().id
	subject = Subject(title, body, author_id)

	profile.subjects.append(subject)	

	db.session.add(subject)    
	db.session.commit()  
	db.session.refresh(subject)

	url = url_for('students.edit_students_profile')
	return redirect(url)   
	
#update selected subject
@sbj.route('/subject_update/<int:selected_subject_id>', methods=['GET', 'POST'])
def subject_update(selected_subject_id):

    subject_select2(selected_subject_id)
		
    subject = Subject.query.get_or_404(selected_subject_id)
    print("In PPPPPPPPPPPPsubject UUUUUUUUUUUUUUUUUUUUUUpdate")
    print(selected_subject_id, subject.id, subject.title)
	
    if request.method == 'GET':
        print("GET render update_subject.html")
        return render_template('update_subject.html', subject=subject)
		
    #get data from form and insert to subjectgress db
    ##import pdb; pdb.set_trace() 	
    subject.title = request.form.get('title')	
    subject.body = request.form.get('body')
    
    db.session.commit()  
    db.session.refresh(subject)
	
    return redirect(url_for('subjectes.edit_subjectes'))
	
		
@sbj.route('/subject_delete_for_good', methods=['GET', 'POST'])
#Here author is user_id
def subject_delete_for_good():
	  
	user = User.query.get_or_404(current_user.id)
	author_id = user.id

	subject = Subject.query.filter(Subject.selected==True).first()
	if subject == None:
		flash("Please select a subject to delete first ")
		return redirect(url_for('select.subject_select'))
			
	print ("delete selected subject is " )
	print(subject.title)      

	db.session.delete(subject) 

	db.session.commit()  

	return redirect(url_for('subjectes.edit_subjectes')) 
		
#delete from index subjectes list
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@sbj.route('/subject_delete_for_good2/<int:selected_subject_id>', methods=['GET', 'POST'])
#Here author is user_id
def subject_delete_for_good2(selected_subject_id):

	print ("SSSSSSSSSSSSSelected subject is" )
	subject_select2(selected_subject_id)
	return redirect(url_for('subjectes.subject_delete_for_good')) 	
