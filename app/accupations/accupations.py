from flask import render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from flask import render_template, flash, redirect, session, url_for, request, jsonify, json
from flask_login import login_user, logout_user, current_user, login_required
#from flask_login import login_manager

from flask_login import LoginManager
from config import basedir
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

from app.models import User, School, Student, Teacher, Profile, Strength, Weakness, Tag, Destination, Goal

from app.forms import LoginForm, EditForm

from sqlalchemy import update

from app.content_management import Content

#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
from flask import Blueprint
acc = Blueprint(
    'accupations', __name__,
    template_folder='templates'
)   
#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
from app.select.select import student_select2, profile_select2, strength_select2, accupation_select2, goal_select2, resource_select2
from app import *
from datetime import datetime


																		

@acc.route('/edit_accupations', methods=['GET', 'POST'])
@login_required
def edit_accupations():
	accupations = Accupation.query.filter(Accupation.hide == False).all()
	#import pdb; pdb.set_trace()
	return render_template('edit_accupations.html', accupations=accupations)							

		
	
@acc.route('/accupation_add', methods=['GET', 'POST'])
def accupation_add():
			
	if request.method == 'GET':
		return render_template('add_accupation.html')
		   
	#get data from form and insert to accupationgress db
	title = request.form.get('title')
	body = request.form.get('description')

	#import pdb; pdb.set_trace() 	
	author_id = current_user._get_current_object().id
	accupation = Accupation(title, body, author_id)	
	    
	db.session.add(accupation)    
	db.session.commit()  
	db.session.refresh(accupation)

	url = url_for('accupations.edit_accupations')
	return redirect(url)   
	
#update selected accupation
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@acc.route('/accupation_update/<int:selected_accupation_id>', methods=['GET', 'POST'])
def accupation_update(selected_accupation_id):

    accupation_select2(selected_accupation_id)
		
    accupation = Accupation.query.get_or_404(selected_accupation_id)
    print("In PPPPPPPPPPPPaccupation UUUUUUUUUUUUUUUUUUUUUUpdate")
    print(selected_accupation_id, accupation.id, accupation.title)
	
    if request.method == 'GET':
        print("GET render update_accupation.html")
        return render_template('update_accupation.html', accupation=accupation)
		
    #get data from form and insert to accupationgress db
    #import pdb; pdb.set_trace() 	
    accupation.title = request.form.get('title')	
    accupation.body = request.form.get('description')
    
    db.session.commit()  
    db.session.refresh(accupation)
	
    return redirect(url_for('accupations.edit_accupations'))
	
		
@acc.route('/accupation_delete_for_good', methods=['GET', 'POST'])
#Here author is user_id
def accupation_delete_for_good():
	  
	print("RRRRRRRRRRRRRRRRRRRRRRRRRR")
	print(g.user)

	user = User.query.get_or_404(g.user.id)
	author_id = user.id

	accupation = Accupation.query.filter(Accupation.selected==True).first()
	if accupation == None:
		flash("Please select a accupation to delete first ")
		return redirect(url_for('select.accupation_select'))
			
	print ("delete selected accupation is " )
	print(accupation.title)      

	goals = Goal.query.join(accupation.goals).filter(accupation.id==accupation.id)
	for goal in goals:
		redirect(url_for('goals.goal_delete2(goal.id)'))
	db.session.delete(accupation) 

	db.session.commit()  

	return redirect(url_for('detinations.edit_accupations')) 
		
#delete from index accupations list
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@acc.route('/accupation_delete_for_good2/<int:selected_accupation_id>', methods=['GET', 'POST'])
#Here author is user_id
def accupation_delete_for_good2(selected_accupation_id):

	print ("SSSSSSSSSSSSSelected accupation is" )
	accupation_select2(selected_accupation_id)
	return redirect(url_for('accupations.accupation_delete_for_good')) 	


@acc.route('/accupation_delete', methods=['GET', 'POST'])
#Here author is user_id
def accupation_delete():
	  
	print("RRRRRRRRRRRRRRRRRRRRRRRRRR")
	print(current_user.id)

	user = User.query.get_or_404(current_user.id)
	author_id = user.id

	accupation = Accupation.query.filter(Accupation.selected==True).first()
	if accupation == None:
		flash("Please select a accupation to delete first ")
		return redirect(url_for('select.accupation_select'))
			
	print ("delete selected accupation is " )
	print(accupation.id)
	
	accupation.hide = True

	db.session.commit()
	#DEBUG
	accupation = Accupation.query.filter(Accupation.selected==True).first()
	print("After commit set hide to True", accupation.id, accupation.hide)
	#DEBUG
	return redirect(url_for('accupations.edit_accupations')) 
		
#delete from index accupations list
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@acc.route('/accupation_delete2/<int:selected_accupation_id>', methods=['GET', 'POST'])
#Here author is user_id
def accupation_delete2(selected_accupation_id):

	print ("SSSSSSSSSSSSSelected accupation is", selected_accupation_id )
	dest = accupation_select2(selected_accupation_id)
	return redirect(url_for('accupations.accupation_delete'))

 	
