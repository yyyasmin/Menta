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
tag = Blueprint(
    'tags', __name__,
    template_folder='templates'
)   
#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
from app.select.select import student_select2, profile_select2, strength_select2, tag_select2, goal_select2, resource_select2
from app import *
from datetime import datetime


																		

@tag.route('/edit_tags', methods=['GET', 'POST'])
@login_required
def edit_tags():
	tags = Tag.query.all()
	##import pdb; pdb.set_trace()
	return render_template('edit_tags.html', tags=tags)							

		
	
@tag.route('/tag_add', methods=['GET', 'POST'])
def tag_add():
			
    if request.method == 'GET':
        return render_template('add_tag.html')
           
    #get data from form and insert to taggress db
    tag_title = request.form.get('tag_title')
    description = request.form.get('description')

    ##import pdb; pdb.set_trace() 	
    #author_id = current_user._get_current_object().id

    author_id = current_user._get_current_object().id
    tag = Tag(tag_title, description, author_id)	
        
    db.session.add(tag)    
    db.session.commit()  
    db.session.refresh(tag)

    url = url_for('tags.edit_tags')
    return redirect(url)   
	
#update selected tag
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@tag.route('/tag_update/<int:selected_tag_id>', methods=['GET', 'POST'])
def tag_update(selected_tag_id):

	tag_select2(selected_tag_id)
	
	tag = Tag.query.filter(Tag.selected==True).first()
	if tag == None:
		flash("Please select a tag to delete first ")
		return redirect(url_for('select.tag_select'))		
	print("In PPPPPPPPPPPPtag UUUUUUUUUUUUUUUUUUUUUUpdate")
	print(selected_tag_id, tag.id, tag.title)

	if request.method == 'GET':
		print("GET render update_tag.html")
		return render_template('update_tag.html', tag=tag)
		
	#get data from form and insert to taggress db
	##import pdb; pdb.set_trace() 	
	tag_title = request.form.get('tag_title')
	tag_age = request.form.get('tag_age')
	description = request.form.get('description')

	db.session.commit()  
	db.session.refresh(tag)

	return redirect(url_for('tags.edit_tags'))
	
		
@tag.route('/tag_delete_for_good', methods=['GET', 'POST'])
#Here author is user_id
def tag_delete_for_good():

	tag = Tag.query.filter(Tag.selected==True).first()
	if tag == None:
		flash("Please select a tag to delete first ")
		return redirect(url_for('select.tag_select'))
			
	print ("delete selected tag is " )
	print("deleting", tag.title)      

	db.session.delete(tag) 
	db.session.commit()  

	return redirect(url_for('tags.edit_tags')) 
		
#delete from index tags list
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@tag.route('/tag_delete_for_good2/<int:selected_tag_id>', methods=['GET', 'POST'])
#Here author is user_id
def tag_delete_for_good2(selected_tag_id):

	print ("SSSSSSSSSSSSSelected tag is" )
	tag_select2(selected_tag_id)
	return redirect(url_for('tags.tag_delete_for_good')) 	


@tag.route('/tag_delete', methods=['GET', 'POST'])
#Here author is user_id
def tag_delete():
	  
	print("RRRRRRRRRRRRRRRRRRRRRRRRRR")
	print(current_user.id)

	user = User.query.get_or_404(current_user.id)
	author_id = user.id

	tag = Tag.selected.filter(Tag.selected==True).first()
	if tag == None:
		flash("Please select a tag to delete first ")
		return redirect(url_for('select.tag_select'))
			
	print ("delete selected tag is " )
	print(tag.id)
	
	tag.hide = True

	db.session.commit()
	#DEBUG
	tag = Tag.selected.filter(Tag.selected==True).first()
	print("After commit set hide to True", tag.id, tag.hide)
	#DEBUG
	return redirect(url_for('tags.edit_tags')) 
		
#delete from index tags list
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@tag.route('/tag_delete2/<int:selected_tag_id>', methods=['GET', 'POST'])
#Here author is user_id
def tag_delete2(selected_tag_id):

	print ("SSSSSSSSSSSSSelected tag is", selected_tag_id )
	dest = tag_select2(selected_tag_id)
	return redirect(url_for('tags.tag_delete'))

 	
