from flask import render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, json
from flask_login import login_user, logout_user, current_user, login_required
#from flask_login import login_manager

from flask_login import LoginManager
from config import basedir
import config

from app import app, db
from app import lm
from .forms import LoginForm

from .models import User, Student, Team_member, Profile, Strength, Weaknesse

from .forms import LoginForm, EditForm

from sqlalchemy import update

from .content_management import Content

from .profile import profile_select2


@app.route('/strengthes_by_profile', methods=['POST', 'GET'])
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

@app.route('/strengthes_by_profile2/<int:selected_profile_id>', methods=['POST', 'GET'])
@login_required
def strengthes_by_profile2(selected_profile_id):
    print("IIn PRRRRRRRRRRRROs AAAAAAAAAAAAAProfile 22222222222222")
    print(selected_profile_id)
    profile_select2(selected_profile_id)
    return redirect(url_for('strengthes_by_profile'))		


@app.route('/strength_select', methods=['GET', 'POST'])
def strength_select():
    print("in ppppppppppppppppstrength_ssssssssssssssssssselect")

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
    	
    #import pdb; pdb.set_trace()

    strengthes = Profile.query.join(Profile.profiles).filter(Profile.id==profile.id)
	

    if (strengthes.count() == 0):
        flash("There is no strengthes for this student.")
        print ("strengthes count is 0 ")
        redirect(url_for('flash_err'))
        return render_template('select_pro.html', strengthes=strengthes)
        #return redirect(url_for('index'))
	
    strength = Strength.query.all()		
    for strength in strengthes:
        strength.selected = False

    if request.method == 'GET':
        return render_template('select_pro.html', strengthes=strengthes)
		
    selected_strength_id = int(request.form['selected_pro'])
    strength = Strength.query.get_or_404(selected_strength_id)
    strength.selected = True
		
    db.session.commit()
    #profiles = Profile.query.all()
    return redirect(url_for('strengthes_by_profile'))		
	


@app.route('/strength_select2/<int:selected_strength_id>', methods=['GET', 'POST'])
def strength_select2(selected_strength_id):

    student = Student.query.filter(Student.selected==True).first()
    if student == None:
        flash("Please select a student first ")
        return redirect(url_for('index'))

    profile = Profile.query.filter(Profile.selected==True).first()    
    if profile == None:
        flash("Please select an profile first ")
        return redirect(url_for('profile_select'))		
    #print request
	
    #import pdb; pdb.set_trace()
    strengthes = Profile.query.join(Profile.strengthes).filter(Profile.id==profile.id)

    if (strengthes.count() == 0):
        flash("There is no strengthes for this student.")
        print ("strengthes count is 0 ")
        redirect(url_for('flash_err'))
        return render_template('select_pro.html', strengthes=strengthes)
		
    profile = Profile.query.filter(Profile.selected==True).first()
    print("In 44444444444444 Begining of strength_select2 profile selected  is:")
    print(profile.id)

    strength = Strength.query.all()		
    for strength in strengthes:
        strength.selected = False
		
    print(profile.id)
    profile_select2(profile.id)    # fixing bug- selected profile was effected by strength select setting
		
    profile = Profile.query.filter(Profile.selected==True).first()
    print("In 55555555555555555  Begining of strength_select2 profile selected  is:")
    print(profile.title)
	
    strength = Strength.query.get_or_404(selected_strength_id)
    print(strength.description)
	
    strength.selected = True
    db.session.commit()
	
    return redirect(url_for('strengthes_by_profile'))		
	

#update selected strength
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@app.route('/strength/update/<int:selected_strength_id>', methods=['GET', 'POST'])
def strength_update(selected_strength_id):

    user = User.query.get_or_404(g.user.id)
    author_id = user.id	
    
    student = Student.query.filter(Student.selected==True).first()
    if student == None:
        flash("Please select a student first ")
        return redirect(url_for('index'))
        
    profile = Profile.query.filter(Profile.selected==True).first()
    print(" In strength_update profile selected is")
    print(profile.title)
    
    if profile == None:
        flash("Please select an profile first ")
        return redirect(url_for('profile_select'))
    print(profile.title)      
    #print request
    
    strength_select2(selected_strength_id)	
    strength = Strength.query.get_or_404(selected_strength_id)
	
    if request.method == 'GET':
        return render_template('update_pro.html', profile=profile, strength=strength)
		
    #get data from form and insert to studentgress db
    #import pdb; pdb.set_trace() 	
    strength.description = request.form.get('description')
    
    db.session.commit()  
    db.session.refresh(strength)
	
    return redirect(url_for('strengthes_by_profile'))		
#end update selected strength 		


		
@app.route('/strengthes/add', methods=['GET', 'POST'])
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
	
@app.route('/strengthes/add/<int:selected_profile_id>', methods=['GET', 'POST'])
def strengthes_add2(selected_profile_id):
    profile_select2(selected_profile_id)
    return redirect(url_for('strengthes_add'))

@app.route('/strength/delete/', methods=['GET', 'POST'])
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
@app.route('/strength/delete2/<int:selected_strength_id>', methods=['GET', 'POST'])
def strength_delete2(selected_strength_id):
    strength_select2(selected_strength_id)
    return redirect(url_for('strength_delete'))
#end profile_delete2
		
