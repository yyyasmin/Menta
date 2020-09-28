from flask import render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, json
from flask_login import login_user, logout_user, current_user, login_required
#from flask_login import login_manager

from flask_login import LoginManager
from config import basedir
import config

from app import  db
from app.models import User, Teacher, Student, Profile, Strength, Weakness, Role

from app.forms import LoginForm, EditForm
from app.select.select import school_select2

from app.templates import *

from sqlalchemy import update

from app.content_management import Content

from sqlalchemy import text # for execute SQL raw SELECT ...


#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
#################
#### imports ####
#################

from flask import Blueprint

from app import forms
#try move to __init__
from app.models import User, School, Teacher, Profile, Strength, Weakness, Role

################
#### config ####
################

scl = Blueprint(
    'schools', __name__,
    template_folder='templates'
) 
from app.select.select import student_select2, teacher_select2
from app import *


@scl.route('/teacher_home' )
@login_required
def school_home():
	print("in teacher_home")
	return render_template('form6.html')

	
@scl.route('/edit_schools')
@login_required
def edit_schools():

    print("")
    print("")
    print ("IN edit_schools ")
    schools = School.query.filter(School.hide==False).all()
    return render_template('edit_schools.html',schools=schools)
                            
                            								
@scl.route('/school_add', methods=['GET', 'POST'])
@login_required
def school_add():

    print("")
    print("")
    print ("IN teacher_add ")    

    author_id = current_user._get_current_object().id
      
    if request.method == 'GET':
        return render_template('add_school.html')
           
    title = request.form.get('title')
    body = request.form.get('body')
    logo_name = request.form.get('logo_name')

    school = School.query.filter(School.title==title).first()
    if school != None:
        flash("בית ספר בשם זה קיים במערכת")
        return edit_schools()

    school = School( title, body, author_id)
    school.logo_name = logo_name
    db.session.add(school)	
      
    db.session.commit()  
    db.session.refresh(school)
    # test insert res
    return edit_schools()


@scl.route('/school_update/<int:selected_school_id>', methods=['GET', 'POST'])
@login_required
def school_update(selected_school_id):
        
    school = school_select2(selected_school_id)
        
    school = School.query.filter(School.id==selected_school_id).first()
    if school==None:
        flash ("אין כזה בית ספר")
        return edit_schools()

    if request.method == 'GET':
        #print("GET render update_teacher.html")
        return render_template('update_school.html', school=school)

    school.title = request.form.get('title')
    school.body = request.form.get('body')
    school.school_logo_name = request.form.get('school_logo_name')
    school.matya_logo_name =  request.form.get('matya_logo_name')

    db.session.commit()  
    db.session.refresh(school)
    return edit_schools()


@scl.route('/school_delete', methods=['GET', 'POST'])
@login_required
def school_delete():

    school = School.query.filter(School.selected==True).first()
    if school == None:
        flash("Please select a school to delete first ")
        return redirect(url_for('select.school_select'))
            
    school.hide = True
    school.selected = False
    db.session.commit()  
    return edit_schools()

	
@scl.route('/school_delete2/<int:selected_school_id>', methods=['GET', 'POST'])
@login_required
def school_delete2(selected_school_id):

	school = school_select2(selected_school_id)
	return school_delete()

	
@scl.route('/dsply_school_logo2/<int:selected_school_id>', methods=['GET', 'POST'])
@login_required
def dsply_school_logo2(selected_school_id):

    school = school_select2(selected_school_id)
    user = current_user._get_current_object()
    user.school_logo_name = school.school_logo_name
    
    school.selected=False
    db.session.commit()
    
    return edit_schools()

	
@scl.route('/dsply_matya_logo2/<int:selected_school_id>', methods=['GET', 'POST'])
@login_required
def dsply_matya_logo2(selected_school_id):

    school = school_select2(selected_school_id)
    user = current_user._get_current_object()
    user.matya_logo_name = school.matya_logo_name
    
    school.selected=False
    db.session.commit()
    
    return edit_schools()
