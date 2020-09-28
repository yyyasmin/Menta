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

from app.models import User, Student, Teacher, Profile, Strength, Weaknesse, Tag, Destination, Goal, Accupation, Due_date

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
	
    #import pdb; pdb.set_trace()
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

	
#update selected strength
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@acc.route('/strength_update/<int:selected_strength_id>', methods=['GET', 'POST'])
def strength_update(selected_strength_id):

    user = User.query.get_or_404(g.user.id)
    author_id = user.id	
    
    strength_select2(selected_strength_id)
		
    strength = strength.query.get_or_404(selected_strength_id)
    print("In PPPPPPPPPPPPstrength UUUUUUUUUUUUUUUUUUUUUUpdate")
    print(selected_strength_id, strength.id, strength.title)
	
    if request.method == 'GET':
        print("GET render update_strength.html")
        return render_template('update_strength.html', strength=strength)
		
    #get data from form and insert to strengthgress db
    #import pdb; pdb.set_trace() 	
    strength.title = request.form.get('title')	
    strength.body = request.form.get('description')
    
    db.session.commit()  
    db.session.refresh(strength)
	
    return redirect(url_for('strengths.edit_strengths'))
#end strength_update
		
@strn.route('/strengthes/add', methods=['GET', 'POST'])
def strengthes_add():

    user = User.query.get_or_404(g.user.id)
    author_id = user.id
	   
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
        return render_template('add_strengthes.html', profile=profile)
           
    #get data from form and insert to studentgress db
    body = request.form.get('description')
	
    #import pdb; pdb.set_trace() 	
    strength = Strength(body)	
	
    profile.strengthes.append(strength)	
	   
    db.session.add(strength)    
    db.session.commit()  
    db.session.refresh(strength)
    # test insert res
    url = url_for('strengthes_by_profile')
    return redirect(url)   
	
@strn.route('/strengthes/add/<int:selected_profile_id>', methods=['GET', 'POST'])
def strengthes_add2(selected_profile_id):
    profile_select2(selected_profile_id)
    return redirect(url_for('strengthes_add'))

@strn.route('/strength/delete/', methods=['GET', 'POST'])
#Here author is user_id
def strength_delete():  
    student = Student.query.filter(Student.selected==True).first()
    print(student.title)
    if student == None:
        flash("Please select a student first ")
        return redirect(url_for('student_select'))
		
    strength = Strength.query.filter(Strength.selected==True).first()
    
    if strength == None:
        flash("Please select a strength to delete first ")
        return redirect(url_for('strength_select'))

    print("deleteint strength %s ", strength.description)		
    db.session.delete(strength)		
    db.session.commit()  
	
    return redirect(url_for('strengthes_by_profile'))
#end profile_delete

		
#profile_delete2
@strn.route('/strength/delete2/<int:selected_strength_id>', methods=['GET', 'POST'])
def strength_delete2(selected_strength_id):
    strength_select2(selected_strength_id)
    return redirect(url_for('strength_delete'))
#end profile_delete2
		
