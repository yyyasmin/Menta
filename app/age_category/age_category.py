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

from app.models import User, School, Student, Teacher, Profile, Strength, Weakness, Tag, Destination, Goal, Age_range

from app.forms import LoginForm, EditForm

from sqlalchemy import update

from app.content_management import Content

#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
from flask import Blueprint
age = Blueprint(
    'age_ranges', __name__,
    template_folder='templates'
)   
#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
from app.select.select import student_select2, profile_select2, strength_select2, age_range_select2, goal_select2, resource_select2
from app import *
from datetime import datetime


																		

@age.route('/edit_age_ranges', methods=['GET', 'POST'])
@login_required
def edit_age_ranges():
    #age_ranges = Age_range.query.filter(Age_range.hide == False).all()
    age_ranges = Age_range.query.all()
    ##import pdb; pdb.set_trace()
    return render_template('edit_age_ranges.html', age_ranges=age_ranges)							

		
	
@age.route('/age_range_add', methods=['GET', 'POST'])
def age_range_add():
			
    if request.method == 'GET':
        return render_template('add_age_range.html')
           
    #get data from form and insert to age_rangegress db
    title = request.form.get('title')
    body = request.form.get('body')
    from_age = int(request.form.get('from_age'))
    to_age = int(request.form.get('to_age'))

    ##import pdb; pdb.set_trace() 	
    author_id = current_user._get_current_object().id
    age_range = Age_range(title, from_age, to_age, author_id)	
    age_range.body = body; 

    db.session.add(age_range)    
    db.session.commit()  
    db.session.refresh(age_range)

    url = url_for('age_ranges.edit_age_ranges')
    return redirect(url)   
	
#update selected age_range
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@age.route('/age_range_update/<int:selected_age_range_id>', methods=['GET', 'POST'])
def age_range_update(selected_age_range_id):

    age_range_select2(selected_age_range_id)
		
    age_range = Age_range.query.get_or_404(selected_age_range_id)
    print("In PPPPPPPPPPPPage_range UUUUUUUUUUUUUUUUUUUUUUpdate")
    print(selected_age_range_id, age_range.id, age_range.title, age_range.from_age, age_range.to_age)
	
    if request.method == 'GET':
        print("GET render update_age_range.html")
        return render_template('update_age_range.html', age_range=age_range)
		
    #get data from form and insert to age_rangegress db
    ##import pdb; pdb.set_trace() 	
    age_range.title = request.form.get('title')	
    age_range.body = request.form.get('body')	
    #import pdb; pdb.set_trace()
    age_range.from_age = int(request.form.get('from_age'))
    age_range.to_age = int(request.form.get('to_age'))

    db.session.commit()  
    db.session.refresh(age_range)
	
    return redirect(url_for('age_ranges.edit_age_ranges'))
	
		
@age.route('/age_range_delete_for_good', methods=['GET', 'POST'])
#Here author is user_id
def age_range_delete_for_good():
	  
    print("IIIIIIIIIIIIIIIInnnn age_range_delete_for_good")
    #import pdb; pdb.set_trace()
    age_range = Age_range.query.filter(Age_range.selected==True).first()
    if age_range == None:
        flash("Please select a age_range to delete first ")
        return redirect(url_for('select.age_range_select'))
            
    print ("delete for good selected age_range is " )
    print(age_range.title)      

    db.session.delete(age_range) 

    db.session.commit()  

    return redirect(url_for('age_ranges.edit_age_ranges')) 
		
#delete from index age_ranges list
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@age.route('/age_range_delete_for_good2/<int:selected_age_range_id>', methods=['GET', 'POST'])
#Here author is user_id
def age_range_delete_for_good2(selected_age_range_id):

    print ("SSSSSSSSSSSSSelected age_range is" )
    #import pdb; pdb.set_trace()
    age_range_select2(selected_age_range_id)
    return redirect(url_for('age_ranges.age_range_delete_for_good')) 	


@age.route('/age_range_delete', methods=['GET', 'POST'])
#Here author is user_id
def age_range_delete():
	  
	print("RRRRRRRRRRRRRRRRRRRRRRRRRR")
	print(current_user.id)

	user = User.query.get_or_404(current_user.id)
	author_id = user.id

	age_range = Age_range.query.filter(Age_range.selected==True).first()
	if age_range == None:
		flash("Please select a age_range to delete first ")
		return redirect(url_for('select.age_range_select'))
			
	print ("delete selected age_range is " )
	print(age_range.id)
	
	age_range.hide = True

	db.session.commit()
	#DEBUG
	age_range = Age_range.query.filter(age_range.selected==True).first()
	print("After commit set hide to True", age_range.id, age_range.hide)
	#DEBUG
	return redirect(url_for('age_ranges.edit_age_ranges')) 
		
#delete from index age_ranges list
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@age.route('/age_range_delete2/<int:selected_age_range_id>', methods=['GET', 'POST'])
#Here author is user_id
def age_range_delete2(selected_age_range_id):

	print ("SSSSSSSSSSSSSelected age_range is", selected_age_range_id )
	dest = age_range_select2(selected_age_range_id)
	return redirect(url_for('age_ranges.age_range_delete'))

 	
