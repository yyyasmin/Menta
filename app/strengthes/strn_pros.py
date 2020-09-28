ffrom flask import render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from flask import render_template, flash, redirect, session, url_for, request, jsonify, json
from flask_login import login_user, logout_user, current_user, login_required
#from flask_login import login_manager

from flask_login import LoginManager
from config import basedir
import config

from app import current_app, db
from app.forms import LoginForm

from app.models import User, School, Student, Teacher, Strengthfile, Strength, Weaknesse

from app.forms import LoginForm, EditForm

from sqlalchemy import update

from app.content_management import Content


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


@app.route('/pro_select', methods=['GET', 'POST'])
def pro_select():
    print("in pppppppppppppppppro_ssssssssssssssssssselect")

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
	
    pro = Strength.query.all()		
    for pro in strengthes:
        pro.selected = False

    if request.method == 'GET':
        return render_template('select_pro.html', strengthes=strengthes)
		
    selected_pro_id = int(request.form['selected_pro'])
    pro = Strength.query.get_or_404(selected_pro_id)
    pro.selected = True
		
    db.session.commit()
    #profiles = Profile.query.all()
    return redirect(url_for('strengthes_by_profile'))		
	


@app.route('/pro_select2/<int:selected_pro_id>', methods=['GET', 'POST'])
def pro_select2(selected_pro_id):

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
    print("In 44444444444444 Begining of pro_select2 profile selected  is:")
    print(profile.id)

    pro = Strength.query.all()		
    for pro in strengthes:
        pro.selected = False
		
    print(profile.id)
    profile_select2(profile.id)    # fixing bug- selected profile was effected by pro select setting
		
    profile = Profile.query.filter(Profile.selected==True).first()
    print("In 55555555555555555  Begining of pro_select2 profile selected  is:")
    print(profile.title)
	
    pro = Strength.query.get_or_404(selected_pro_id)
    print(pro.description)
	
    pro.selected = True
    db.session.commit()
	
    return redirect(url_for('strengthes_by_profile'))		
	

#update selected pro
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@app.route('/pro/update/<int:selected_pro_id>', methods=['GET', 'POST'])
def pro_update(selected_pro_id):

    user = User.query.get_or_404(g.user.id)
    author_id = user.id	
    
    student = Student.query.filter(Student.selected==True).first()
    if student == None:
        flash("Please select a student first ")
        return redirect(url_for('index'))
        
    profile = Profile.query.filter(Profile.selected==True).first()
    print(" In pro_update profile selected is")
    print(profile.title)
    
    if profile == None:
        flash("Please select an profile first ")
        return redirect(url_for('profile_select'))
    print(profile.title)      
    #print request
    
    pro_select2(selected_pro_id)	
    pro = Strength.query.get_or_404(selected_pro_id)
	
    if request.method == 'GET':
        return render_template('update_pro.html', profile=profile, pro=pro)
		
    #get data from form and insert to studentgress db
    #import pdb; pdb.set_trace() 	
    pro.description = request.form.get('description')
    
    db.session.commit()  
    db.session.refresh(pro)
	
    return redirect(url_for('strengthes_by_profile'))		
#end update selected pro 		


		
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
    pro = Strength(body)	
	
    profile.strengthes.append(pro)	
	   
    db.session.add(pro)    
    db.session.commit()  
    db.session.refresh(pro)
    # test insert res
    url = url_for('strengthes_by_profile')
    return redirect(url)   
	
@app.route('/strengthes/add/<int:selected_profile_id>', methods=['GET', 'POST'])
def strengthes_add2(selected_profile_id):
    profile_select2(selected_profile_id)
    return redirect(url_for('strengthes_add'))

@app.route('/pro/delete/', methods=['GET', 'POST'])
#Here author is user_id
def pro_delete():  
    student = Student.query.filter(Student.selected==True).first()
    print(student.title)
    if student == None:
        flash("Please select a student first ")
        return redirect(url_for('student_select'))
		
    pro = Strength.query.filter(Strength.selected==True).first()
    
    if pro == None:
        flash("Please select a pro to delete first ")
        return redirect(url_for('pro_select'))

    print("deleteint pro %s ", pro.description)		
    db.session.delete(pro)		
    db.session.commit()  
	
    return redirect(url_for('strengthes_by_profile'))
#end profile_delete

		
#profile_delete2
@app.route('/pro/delete2/<int:selected_pro_id>', methods=['GET', 'POST'])
def pro_delete2(selected_pro_id):
    pro_select2(selected_pro_id)
    return redirect(url_for('pro_delete'))
#end profile_delete2
		
