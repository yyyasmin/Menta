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
sts = Blueprint(
    'status', __name__,
    template_folder='templates'
)   
#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
from app.select.select import student_select2, profile_select2, strength_select2, status_select2, goal_select2, resource_select2
from app import *
from datetime import datetime

																		
@sts.route('/edit_statuses', methods=['GET', 'POST'])
@login_required
def edit_statuses():
	statuses = Status.query.filter(Status.hide == False).all()
	##import pdb; pdb.set_trace()
	return render_template('edit_statuses.html', statuses=statuses)							

			
@sts.route('/status_add', methods=['GET', 'POST'])
def status_add():

    #import pdb; pdb.set_trace()
    
    if request.method == 'GET':
        return render_template('add_status.html')
           
    #get data from form and insert to statusgress db
    title = request.form.get('title')
    body = request.form.get('description')    
    color = request.form.get('color')

    ##import pdb; pdb.set_trace() 	
    author_id = current_user._get_current_object().id
        
    status = Status.query.filter(Status.title==title).first()
    if status == None:
        status = Status(title, body, author_id)	
                                
    if color=='אדום':
        status.color = '#ff0000'
    elif color=='כחול':
        status.color = '#0000cc'
    elif color=='צהוב':
        status.color = '#ffcc00'
    elif color=='כתום':
        status.color = '#ff981a'            
    elif color=='ירוק':
        status.color = '#00b300'

    elif color=='lblue':
        status.color = '#e6ffff'
    elif color=='lyellow':
        status.color = '#ffffcc'
    elif color=='lorange':
        status.color = '#ffcc66'            
    elif color=='lgreen':
        status.color = '#ccffcc'
    elif color=='lred':
        status.color = '#ffcccc'        
    elif color=='lpurple':
        status.color = '#ffe6ff'        

    elif color=='red':
        status.color = '#ff0000'
    elif color=='blue':
        status.color = '#0000cc'
    elif color=='yellow':
        status.color = '#ffcc00'
    elif color=='orange':
        status.color = '#ff981a'            
    elif color=='green':
        status.color = '#00b300'        
    elif color=='purple':
        status.color = '#cc00cc'        

    else:
        status.color = '#000000'
    
    db.session.add(status)    
    db.session.commit()  

    url = url_for('status.edit_statuses')
    return redirect(url)   

#update selected status
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@sts.route('/status_update/<int:selected_status_id>', methods=['GET', 'POST'])
def status_update(selected_status_id):
    ##import pdb; pdb.set_trace()
    status = status_select2(selected_status_id)
		
    print("In PPPPPPPPPPPPstatus UUUUUUUUUUUUUUUUUUUUUUpdate")
    print(selected_status_id, status.id, status.title)
	
    if request.method == 'GET':
        print("GET render update_status.html")
        return render_template('update_status.html', status=status)
		
    #get data from form and insert to statusgress db
    ###import pdb; pdb.set_trace() 	
    status.title = request.form.get('title')	
    status.body = request.form.get('description')
    
    color = request.form.get('color')
    
    if color=='אדום':
        status.color = '#ff0000'
    if color=='כחול':
        status.color = '#0000cc'
    if color=='צהוב':
        status.color = '#ffcc00'
    if color=='ירוק':
        status.color = '#00b300'

    
    db.session.commit()  
    db.session.refresh(status)
	
    return redirect(url_for('status.edit_statuses'))
	
		
@sts.route('/status_delete_for_good', methods=['GET', 'POST'])
#Here author is user_id
def status_delete_for_good():
	  
	print("RRRRRRRRRRRRRRRRRRRRRRRRRR")
	print(g.user)

	user = User.query.get_or_404(g.user.id)
	author_id = user.id

	status = status.query.filter(status.selected==True).first()
	if status == None:
		flash("Please select a status to delete first ")
		return redirect(url_for('select.status_select'))
			
	print ("delete selected status is " )
	print(status.title)      

	goals = Goal.query.join(status.goals).filter(status.id==status.id)
	for goal in goals:
		redirect(url_for('goals.goal_delete2(goal.id)'))
	db.session.delete(status) 

	db.session.commit()  

	return redirect(url_for('detinations.edit_statuses')) 
		
#delete from index statuses list
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@sts.route('/status_delete_for_good2/<int:selected_status_id>', methods=['GET', 'POST'])
#Here author is user_id
def status_delete_for_good2(selected_status_id):

	print ("SSSSSSSSSSSSSelected status is" )
	status_select2(selected_status_id)
	return redirect(url_for('status.status_delete_for_good')) 	


@sts.route('/status_delete', methods=['GET', 'POST'])
#Here author is user_id
def status_delete():
	  
	print("RRRRRRRRRRRRRRRRRRRRRRRRRR")
	print(current_user.id)

	user = User.query.get_or_404(current_user.id)
	author_id = user.id

	status = status.query.filter(status.selected==True).first()
	if status == None:
		flash("Please select a status to delete first ")
		return redirect(url_for('select.status_select'))
			
	print ("delete selected status is " )
	print(status.id)
	
	status.hide = True

	db.session.commit()
	#DEBUG
	status = status.query.filter(status.selected==True).first()
	print("After commit set hide to True", status.id, status.hide)
	#DEBUG
	return redirect(url_for('status.edit_statuses')) 
		
#delete from index statuses list
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@sts.route('/status_delete2/<int:selected_status_id>', methods=['GET', 'POST'])
#Here author is user_id
def status_delete2(selected_status_id):

	print ("SSSSSSSSSSSSSelected status is", selected_status_id )
	dest = status_select2(selected_status_id)
	return redirect(url_for('status.status_delete'))

 	
