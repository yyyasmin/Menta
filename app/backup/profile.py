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

from .students import student_select2



@app.route('/profile_select', methods=['GET', 'POST'])
def profile_select():
    print("in profile_select")

    student = Student.query.filter(Student.selected==True).first()
    if student == None:
        flash("Please select a student first ")
        return redirect(url_for('index'))
    print("in profile_select")
	
    #import pdb; pdb.set_trace()

    profile = Profile.query.join(Student.profile).filter(Student.id==student.id)

    if (profile.count() == 0):
        flash("There is no profile for this student.")
        print ("profile count is 0 ")
        redirect(url_for('flash_err'))
        return render_template('select_profile.html', profile=profile)
        #return redirect(url_for('index'))
		
    profile = Profile.query.all()			
    for profile in profile:
        print("In profile_select seting profile %s to False", profile.title)
        pribr(profile.title)
        profile.selected = False

    if request.method == 'GET':
        return render_template('select_profile.html', profile=profile)
		
    selected_profile_id = int(request.form['selected_profile'])
    print (selected_profile_id)
    profile = Profile.query.get_or_404(selected_profile_id)
    print("In profile_select seting profile %s to True", profile.title)
    pribr(profile.title)
    profile.selected = True
    print(profile.title)
    db.session.commit()
    profile = Profile.query.get_or_404(selected_profile_id)
    print(profile.selected)
    #profile = Profile.query.all()
    print("end profile_select calling render_template show_selected_profile ")
    print("")
    return render_template('show_selected_profile.html', profile=profile)
	


@app.route('/profile_select2/<int:selected_profile_id>', methods=['GET', 'POST'])
def profile_select2(selected_profile_id):
    print("IIIIIIIIIIIIIIIIn profile_select2")
    print(selected_profile_id)
    student = Student.query.filter(Student.selected==True).first()
    if student == None:
        flash("Please select a student first ")
        return redirect(url_for('index'))
    print("in profile_select")
	
    #import pdb; pdb.set_trace()

    profile = Profile.query.join(Student.profile).filter(Student.id==student.id)

    if (profile.count() == 0):
        flash("There is no profile for this student.")
        print ("profile count is 0 ")
        redirect(url_for('flash_err'))
        return render_template('select_profile.html', profile=profile)
        #return redirect(url_for('index'))
		
    profile = Profile.query.all()		
    for profile in profile:
        print("In profile_select2 seting profile %s to False", profile.title)
        print(profile.title)
        profile.selected = False

    print(selected_profile_id)
    profile = Profile.query.get_or_404(selected_profile_id)
    print("In profile_select2 seting profile %s to True", profile.title)
    print(profile.title)
    profile.selected = True
	
    db.session.flush()
    db.session.commit()
    db.session.refresh(profile)
	
    profile = Profile.query.filter(Profile.selected==True).first()

    print("end of profile_select2 before calling profile_by_student   profile selected is  %s", profile.title)
    print(profile.title)	
    return redirect(url_for('profile_by_student'))	
    print("")	
    #return render_template('show_selected_profile.html', profile=profile)
	
		
@app.route('/profile_by_student', methods=['POST', 'GET'])
@login_required
def profile_by_student():
	
    #import pdb; pdb.set_trace()
    student = Student.query.filter(Student.selected==True).first()

    if student == None:
        flash("Please select a student first ")
        return redirect(url_for('index'))
		
    print("student")
    print(student.title)
	
    profile = Profile.query.join(Student.profile).filter(Student.id==student.id)
		
    return render_template('show_student_profile2.html',
                            student=student,
                            profile=profile
							)
	
@app.route('/profile_by_student2/<int:selected_student_id>', methods=['POST', 'GET'])
@login_required
def profile_by_student2(selected_student_id):
    student_select2(selected_student_id)
    return redirect(url_for('profile_by_student'))			


@app.route('/profile/add', methods=['GET', 'POST'])
def profile_add():

    user = User.query.get_or_404(g.user.id)
    author_id = user.id
         
    student = Student.query.filter(Student.selected==True).first()
    print(student.title)
    if student == None:
        flash("Please select a student first ")
        return redirect(url_for('student_select'))
   
    #print request
    
    if request.method == 'GET':
        return render_template('add_profile.html', student=student)
           
    #get data from form and insert to studentgress db
    title = request.form.get('title')
    body = request.form.get('description')
	
    #import pdb; pdb.set_trace() 	
    profile = Profile(title, body, author_id)	
	
    student.profile.append(profile)	
	   
    db.session.add(profile)    
    db.session.commit()  
    db.session.refresh(profile)
    # test insert res
    url = url_for('profile_by_student')
    return redirect(url)   
	

@app.route('/profile2/add/<int:selected_student_id>', methods=['GET', 'POST'])
def profile_add2(selected_student_id):
   print(selected_student_id)
   student_select2(selected_student_id)
   return profile_add()
 

#update selected profile
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@app.route('/profile2/update/<int:selected_profile_id>', methods=['GET', 'POST'])
def profile_update(selected_profile_id):

    student = Student.query.filter(Student.selected==True).first()
    print(student.username)
    if student == None:
        flash("Please select a student first ")
        return redirect(url_for('student_select'))
   
    profile_select2(selected_profile_id)
		
    profile = Profile.query.get_or_404(selected_profile_id)
    if request.method == 'GET':
        return render_template('update_profile.html', student=student, profile=profile)
		
    #get data from form and insert to studentgress db
    #import pdb; pdb.set_trace() 	
    profile.title = request.form.get('title')	
    profile.body = request.form.get('description')
    
    db.session.commit()  
    db.session.refresh(profile)
	
    return redirect(url_for('profile_by_student'))			
#end update selected profile 		


@app.route('/profile/delete/', methods=['GET', 'POST'])
#Here author is user_id
def profile_delete():
      
    student = Student.query.filter(Student.selected==True).first()
    print(student.title)
    if student == None:
        flash("Please select a student first ")
        return redirect(url_for('student_select'))
		
    profile = Profile.query.filter(Profile.selected==True).first()
    
    if profile == None:
        flash("Please select an profile first ")
        return redirect(url_for('profile_select'))
		
    #print request
    pros = Pro.query.join(Profile.pros).filter(Profile.id==profile.id)
    cons = Weakennes.query.join(Profile.cons).filter(Profile.id==profile.id)
  

    for pro in pros:		
            print(pro.description)
            db.session.delete(pro)
    for weaknnese in cons:
            print(weaknnese.description)
            db.session.delete(weaknnese)
			
    db.session.delete(profile)			
    db.session.commit()  
	
    return redirect(url_for('profile_by_student'))
#end profile_delete

		
#profile_delete2
@app.route('/profile/delete2/<int:selected_profile_id>', methods=['GET', 'POST'])
def profile_delete2(selected_profile_id):

    profile_select2(selected_profile_id)
    return profile_delete()
#end profile_delete2
		
#profile

							   					
