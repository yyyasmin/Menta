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


@app.route('/weaknesses_by_profile', methods=['POST', 'GET'])
@login_required
def weaknesses_by_profile():
	
    student = Student.query.filter(Student.selected==True).first()
    if student == None:
        flash("Please select a student first ")
        return redirect(url_for('index'))
	
    profile = Profile.query.filter(Profile.selected==True).first()
    print("in weaknesses_by_profile profile selected is")
    print(profile.title)
    if profile == None:
        flash("Please select an profile first ")
        return redirect(url_for('profile_select'))
	
    #import pdb; pdb.set_trace()
    cons = Con.query.join(Profile.cons).filter(Profile.id==profile.id)
    return render_template('show_profile_cons2.html',
                            student=student,
                            profile=profile,
                            cons=cons
							)

@app.route('/weaknesses_by_profile2/<int:selected_profile_id>', methods=['POST', 'GET'])
@login_required
def weaknesses_by_profile2(selected_profile_id):
    print("IIn PRRRRRRRRRRRROs AAAAAAAAAAAAAProfile 22222222222222")
    print(selected_profile_id)
    profile_select2(selected_profile_id)
    return redirect(url_for('weaknesses_by_profile'))		


@app.route('/weaknesse_select', methods=['GET', 'POST'])
def weaknesse_select():
    print("in ppppppppppppppppweaknesse_ssssssssssssssssssselect")

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

    cons = Profile.query.join(Profile.profiles).filter(Profile.id==profile.id)
	

    if (cons.count() == 0):
        flash("There is no cons for this student.")
        print ("cons count is 0 ")
        redirect(url_for('flash_err'))
        return render_template('select_con.html', cons=cons)
        #return redirect(url_for('index'))
	
    con = Con.query.all()		
    for con in cons:
        con.selected = False

    if request.method == 'GET':
        return render_template('select_con.html', cons=cons)
		
    selected_weaknesse_id = int(request.form['selected_con'])
    con = Con.query.get_or_404(selected_weaknesse_id)
    con.selected = True
		
    db.session.commit()
    #profiles = Profile.query.all()
    return redirect(url_for('weaknesses_by_profile'))		
	


@app.route('/weaknesse_select2/<int:selected_weaknesse_id>', methods=['GET', 'POST'])
def weaknesse_select2(selected_weaknesse_id):

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
    cons = Profile.query.join(Profile.cons).filter(Profile.id==profile.id)

    if (cons.count() == 0):
        flash("There is no cons for this student.")
        print ("cons count is 0 ")
        redirect(url_for('flash_err'))
        return render_template('select_con.html', cons=cons)
		
    profile = Profile.query.filter(Profile.selected==True).first()
    print("In 44444444444444 Begining of weaknesse_select2 profile selected  is:")
    print(profile.id)

    con = Con.query.all()		
    for con in cons:
        con.selected = False
		
    print(profile.id)
    profile_select2(profile.id)    # fixing bug- selected profile was effected by con select setting
		
    profile = Profile.query.filter(Profile.selected==True).first()
    print("In 55555555555555555  Begining of weaknesse_select2 profile selected  is:")
    print(profile.title)
	
    con = Con.query.get_or_404(selected_weaknesse_id)
    print(con.description)
	
    con.selected = True
    db.session.commit()
	
    return redirect(url_for('weaknesses_by_profile'))		
	

#update selected con
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@app.route('/con/update/<int:selected_weaknesse_id>', methods=['GET', 'POST'])
def weaknesse_update(selected_weaknesse_id):

    user = User.query.get_or_404(g.user.id)
    author_id = user.id	
    
    student = Student.query.filter(Student.selected==True).first()
    if student == None:
        flash("Please select a student first ")
        return redirect(url_for('index'))
        
    profile = Profile.query.filter(Profile.selected==True).first()
    print(" In weaknesse_update profile selected is")
    print(profile.title)
    
    if profile == None:
        flash("Please select an profile first ")
        return redirect(url_for('profile_select'))
    print(profile.title)      
    #print request
    
    weaknesse_select2(selected_weaknesse_id)	
    con = Con.query.get_or_404(selected_weaknesse_id)
	
    if request.method == 'GET':
        return render_template('update_con.html', profile=profile, con=con)
		
    #get data from form and insert to studentgress db
    #import pdb; pdb.set_trace() 	
    con.description = request.form.get('description')
    
    db.session.commit()  
    db.session.refresh(con)
	
    return redirect(url_for('weaknesses_by_profile'))		
#end update selected con 		


		
@app.route('/cons/add', methods=['GET', 'POST'])
def weaknesses_add():
    print("IIIIIn CCCCCCCCCCCCons AAAAAAAAAAAAAAAAAd")
    user = User.query.get_or_404(g.user.id)
    author_id = user.id
	
    
    student = Student.query.filter(Student.selected==True).first()
    if student == None:
        flash("PPPPPPPPPPPPPPPPPPPPPPlease select a student first ")
        return redirect(url_for('index'))
        
    profile = Profile.query.filter(Profile.selected==True).first()
    
    if profile == None:
        flash("PPPPPPPPPPPPlease select an aaaaccccttttiiiiooooonnnnnn first ")
        return redirect(url_for('profile_select'))
    print(profile.title)      
    
    if request.method == 'GET':
        return render_template('add_cons.html', profile=profile)
           
    #get data from form and insert to studentgress db
	
    body = request.form.get('description')
	
    con = Con(body)	
    profile.cons.append(con)	
	   
    db.session.add(con)    
    db.session.commit()  
    db.session.refresh(con)
    url = url_for('weaknesses_by_profile')
    return redirect(url)   
	
@app.route('/cons/add/<int:selected_profile_id>', methods=['GET', 'POST'])
def weaknesses_add2(selected_profile_id):
    profile_select2(selected_profile_id)
	#import pdb; pdb.set_trace()
    return redirect(url_for('weaknesses_add'))

@app.route('/con/delete/', methods=['GET', 'POST'])
#Here author is user_id
def weaknesse_delete():  
    student = Student.query.filter(Student.selected==True).first()
    print(student.title)
    if student == None:
        flash("Please select a student first ")
        return redirect(url_for('student_select'))
		
    con = Con.query.filter(Con.selected==True).first()
    
    if con == None:
        flash("Please select a con to delete first ")
        return redirect(url_for('weaknesse_select'))

    print("deleteint con %s ", con.description)		
    db.session.delete(con)		
    db.session.commit()  
	
    return redirect(url_for('weaknesses_by_profile'))
#end profile_delete

		
#profile_delete2
@app.route('/con/delete2/<int:selected_weaknesse_id>', methods=['GET', 'POST'])
def weaknesse_delete2(selected_weaknesse_id):
    weaknesse_select2(selected_weaknesse_id)
    return redirect(url_for('weaknesse_delete'))
#end profile_delete2
		
