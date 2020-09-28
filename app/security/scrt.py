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

from app.models import User, School, Student, Teacher  
from app.models import Profile, Strength, Weakness
from app.models import Tag, Destination, Goal, Age_range, Scrt


from app.forms import LoginForm, EditForm

from sqlalchemy import update

from app.content_management import Content

#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
from flask import Blueprint
scrt = Blueprint(
    'scrts', __name__,
    template_folder='templates'
)   
#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
from app.select.select import student_select2, profile_select2, strength_select2, scrt_select2, goal_select2, resource_select2
from app import *
from datetime import datetime


																		

@scrt.route('/edit_scrts', methods=['GET', 'POST'])
@login_required
def edit_scrts():
    #scrts = Scrt.query.filter(Scrt.hide == False).all()
    scrts = Scrt.query.all()
    ##import pdb; pdb.set_trace()
    return render_template('edit_scrts.html', scrts=scrts)							

		
	
@scrt.route('/scrt_add', methods=['GET', 'POST'])
def scrt_add():
			
    if request.method == 'GET':
        return render_template('add_scrt.html')
           
    #get data from form and insert to scrtgress db
    title = request.form.get('title')
    body = request.form.get('body')

    ##import pdb; pdb.set_trace() 	
    author_id = current_user._get_current_object().id
    scrt = Scrt(title, body, author_id)	

    db.session.add(scrt)    
    db.session.commit()  
    db.session.refresh(scrt)

    url = url_for('scrts.edit_scrts')
    return redirect(url)   
	
#update selected scrt
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@scrt.route('/scrt_update/<int:selected_scrt_id>', methods=['GET', 'POST'])
def scrt_update(selected_scrt_id):

    scrt_select2(selected_scrt_id)
		
    scrt = Scrt.query.get_or_404(selected_scrt_id)
    print("In PPPPPPPPPPPPscrt UUUUUUUUUUUUUUUUUUUUUUpdate")
    print(selected_scrt_id, scrt.id, scrt.title, scrt.from_age, scrt.to_age)
	
    if request.method == 'GET':
        print("GET render update_scrt.html")
        return render_template('update_scrt.html', scrt=scrt)
		
    #get data from form and insert to scrtgress db
    ##import pdb; pdb.set_trace() 	
    scrt.title = request.form.get('title')	
    scrt.body = request.form.get('body')	
    ##import pdb; pdb.set_trace()

    db.session.commit()  
    db.session.refresh(scrt)
	
    return redirect(url_for('scrts.edit_scrts'))
	
		
@scrt.route('/scrt_delete_for_good', methods=['GET', 'POST'])
#Here author is user_id
def scrt_delete_for_good():
	  
    print("IIIIIIIIIIIIIIIInnnn scrt_delete_for_good")
    #import pdb; pdb.set_trace()
    scrt = Scrt.query.filter(Scrt.selected==True).first()
    if scrt == None:
        flash("Please select a scrt to delete first ")
        return redirect(url_for('select.scrt_select'))
            
    print ("delete for good selected scrt is " )
    print(scrt.title)      

    db.session.delete(scrt) 

    db.session.commit()  

    return redirect(url_for('scrts.edit_scrts')) 
		
#delete from index scrts list
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@scrt.route('/scrt_delete_for_good2/<int:selected_scrt_id>', methods=['GET', 'POST'])
#Here author is user_id
def scrt_delete_for_good2(selected_scrt_id):

    print ("SSSSSSSSSSSSSelected scrt is" )
    #import pdb; pdb.set_trace()
    scrt_select2(selected_scrt_id)
    return redirect(url_for('scrts.scrt_delete_for_good')) 	


@scrt.route('/scrt_delete', methods=['GET', 'POST'])
#Here author is user_id
def scrt_delete():
	  
	print("RRRRRRRRRRRRRRRRRRRRRRRRRR")
	print(current_user.id)

	user = User.query.get_or_404(current_user.id)
	author_id = user.id

	scrt = Scrt.query.filter(Scrt.selected==True).first()
	if scrt == None:
		flash("Please select a scrt to delete first ")
		return redirect(url_for('select.scrt_select'))
			
	print ("delete selected scrt is " )
	print(scrt.id)
	
	scrt.hide = True

	db.session.commit()
	#DEBUG
	scrt = Scrt.query.filter(scrt.selected==True).first()
	print("After commit set hide to True", scrt.id, scrt.hide)
	#DEBUG
	return redirect(url_for('scrts.edit_scrts')) 
		
#delete from index scrts list
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@scrt.route('/scrt_delete2/<int:selected_scrt_id>', methods=['GET', 'POST'])
#Here author is user_id
def scrt_delete2(selected_scrt_id):

	print ("SSSSSSSSSSSSSelected scrt is", selected_scrt_id )
	dest = scrt_select2(selected_scrt_id)
	return redirect(url_for('scrts.scrt_delete'))

 	
