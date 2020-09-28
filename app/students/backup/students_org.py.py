from flask import render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, json
from flask_login import login_user, logout_user, current_user, login_required
#from flask_login import login_manager

from flask_login import LoginManager
from config import basedir
import config

from app import  db
from app.models import User, Student, Teacher, Profile, Strength, Weakness, Role

from app.forms import LoginForm, EditForm

from app.select.select import teacher_select2, student_select2
from app.select.select import destination_select2, goal_select2, todo_select2, std_goal_select2, document_select2
from app.select.select import profile_select2, strength_select2, subject_select2, weakness_select2


from app.forms import LoginForm, EditForm

from app.templates import *

from sqlalchemy import update

from app.content_management import Content

from sqlalchemy import text # for execute SQL raw SELECT ...

from datetime import date


#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
#################
#### imports ####
#################

from flask import Blueprint

from app import forms
#try move to __init__
from app.models import User, School, Student, Profile, Strength, Weakness, Role

################
#### config ####
################

std = Blueprint(
    'students', __name__,
    template_folder='templates'
) 
from app.select.select import teacher_select2, student_select2, todo_select2
from app import *

@std.route('/')
@std.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    current_user.__repr__()

    print( current_user.__repr__() )

    #Reset student selection
    students = Student.query.all()
    for std in students:
        ##print("IN INDExxxxxxxxxxxxxxxxxxxxx UUU nselectingstd: ", std.id)
        std.selected = False
    db.session.commit() 
    #Reset student selection

    students = Student.query.filter(Student.hide == False).all()
    ##print("SSSSSSSSSSSSSSSSSSSSSSSStdnts")
    ##print (students)

    return render_template('try_img_ratio.html')


@std.route('/student_home' )
@login_required
def student_home():
	#print("in student_home")
	return render_template('try_img_ratio.html')
	
		
@std.route('/show_student_tree', methods=['GET', 'POST'])
@login_required
def show_student_tree():

    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student to delete first ")
        return redirect(url_for('students.edit_students'))
 
    return render_template('show_students_tree.html', student=std)
    #return render_template('./backup/dbg_inspector_frame.html', student=std)
    #return render_template('./backup/ft_1.html', student=std)
    
    
@std.route('/show_student_tree2/<int:selected_student_id>', methods=['GET', 'POST'])
@login_required
def show_student_tree2(selected_student_id):
	##print ("SSSSSSSSSSSSSelected student is" )
	std = student_select2(selected_student_id)
	return redirect(url_for('students.show_student_tree'))

	
@std.route('/edit_students')
@login_required
def edit_students():
    #students = Student.query.filter(Student.id != 0).all()
    students = Student.query.filter(Student.hide==False).all()
    return render_template('edit_students3.html',
                            students=students
                            )
							
							
@std.route('/get_dummy_student', methods=['GET', 'POST'])
def get_dummy_student():
	###########################impor pdb;pdb.set_trace()
	dummy_std = Student.query.filter(Student.id==0).first()
	#print(dummy_std)
	###########################impor pdb;pdb.set_trace()
	if dummy_std:
		#print ("returng dummy ", dummy_std, dummy_std.id)
		return dummy_std
	else:
		#print("dummy_std does not exist creating new one dummy_std is: ", dummy_std)
		dummy_std = Student(0, 'Humpty', 'Dumpty', date.today(), 'D')
		dummy_std.hide=True
		db.session.add(dummy_std)	
		db.session.commit()  
		db.session.refresh(dummy_std)
		#print("Created dummy std id first_name: ", dummy_std.id, dummy_std.first_name)
	return dummy_std
								
@std.route('/student_add', methods=['GET', 'POST'])
@login_required
def student_add():
      
    ##print("RRRRRRRRRRRRRRRRRRRRRRRRRR")
    user = User.query.get_or_404( current_user._get_current_object().id)
    ##print(current_user._get_current_object().id)

    ###print request

    if request.method == 'GET':
        return render_template('add_student.html', user=user)
           
    #get data from form and insert to student in studentgress  db
    id = request.form.get('id')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    birth_date = request.form.get('birth_date')
    grade = request.form.get('grade')
    background = request.form.get('background')

    student_already_exist = Student.query.filter(Student.id == id).first()
    ###########################impor pdb;pdb.set_trace()
    #print(student_already_exist)
    if student_already_exist is not None :  #Student already exist in system probably in hide mode
        flash("This student already exists in system", student_already_exist.id)
        return render_template('un_hide_student.html', student_already_exist=student_already_exist)

    #############################impor pdb;pdb.set_trace() 	Enter new student to DB
    student = Student(id, first_name, last_name, birth_date, grade)	

    student.background = background

    new_profile = Profile('New profile', 'No description yet')
    db.session.add(new_profile)	
    db.session.commit() 	
    db.session.refresh(new_profile)
    ###########################impor pdb;pdb.set_trace()
    #print(new_profile.id)
    student.profile_id = new_profile.id

    db.session.add(student)	
    db.session.commit()  
    db.session.refresh(student)

    url = url_for('students.edit_students')
    return redirect(url)   


@std.route('/student_unhide2/<int:selected_student_id>', methods=['GET', 'POST'])
#Here author is user_id
@login_required
def student_unhide2(selected_student_id):
	  
	##print("In UUUUUUUUUUUnhide2 student    method", selected_student_id, request.method)
	user = User.query.get_or_404(current_user._get_current_object().id)
	#print(current_user._get_current_object().id)

	###print request		
	student = Student.query.filter(Student.id==selected_student_id).first()
	student.hide = False
	db.session.commit()  
	db.session.refresh(student)
	url = url_for('students.edit_students')
	return redirect(url)


	
#update selected student
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@std.route('/student_update/<int:selected_student_id>', methods=['GET', 'POST'])
@login_required
def student_update(selected_student_id):

	std = student_select2(selected_student_id)
		
	student = Student.query.get_or_404(selected_student_id)
	if request.method == 'GET':
		return render_template('update_student.html', student=student)
  
	student.first_name = request.form.get('first_name')
	student.ltagast_name = request.form.get('last_name')

	student.birth_date = request.form.get('birth_date')
	student.grade = request.form.get('grade')
	student.background = request.form.get('background')
	
	db.session.commit()  
	db.session.refresh(student)
	url = url_for('students.edit_students')
	return redirect(url)   	
	
		
@std.route('/student_delete', methods=['GET', 'POST'])
#Here author is user_id
@login_required
def student_delete():
	  
	##print("RRRRRRRRRRRRRRRRRRRRRRRRRR")
	#print(current_user._get_current_object().id)

	user = User.query.get_or_404(current_user._get_current_object().id)
	author_id = user.id
	
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student to delete first ")
		return redirect(url_for('students.edit_students'))
			
	student.hide = True
	db.session.commit()  

	return redirect(url_for('students.edit_students')) 
		
#delete from index students list
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@std.route('/student_delete2/<int:selected_student_id>', methods=['GET', 'POST'])
#Here author is user_id
@login_required
def student_delete2(selected_student_id):

	##print ("SSSSSSSSSSSSSelected student is", selected_student_id )
	std = student_select2(selected_student_id)
	##print(" IN student_delete2 dddddddddeleting student :", std.id)
	return student_delete()



@std.route('/student_delete_for_good', methods=['GET', 'POST'])
#Here author is user_id
@login_required
def student_delete_for_good():
	  
	##print("RRRRRRRRRRRRRRRRRRRRRRRRRR")
	#print(current_user._get_current_object().id)

	user = User.query.get_or_404(current_user._get_current_object().id)
	author_id = user.id
	
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student to delete first ")
		return redirect(url_for('students.edit_students'))
			
	db.session.delete(student)
	db.session.commit()  

	return redirect(url_for(edit_students)) 
		
#delete from index students list
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@std.route('/student_delete_for_good2/<int:selected_student_id>', methods=['GET', 'POST'])
#Here author is user_id
@login_required
def student_delete_for_good2(selected_student_id):

	##print ("SSSSSSSSSSSSSelected student is", selected_student_id )
	std = student_select2(selected_student_id)
	##print(" IN student_delete2 dddddddddeleting student :", std.id)
	return student_delete_for_good()

##############START studets plan report###############
	
@std.route('/plan_report', methods=['GET', 'POST'])
@login_required
def plan_report():

    print("In plan report ")
    ################import_pdb; pdb.set_trace()
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))

    student_staff_teachers = get_student_teachers()
    tags = Tag.query.filter(Tag.hide == False).all()
    profile = Profile.query.filter(std.profile_id == Profile.id).first()

    std_goals = Std_goal.query.filter(Std_goal.student_id == std.id).all()

    return render_template('plan_report/plan_report.html',  
                                            student=std,
                                            std_goals=std_goals,
                                            student_staff_teachers=student_staff_teachers,
                                            tags=tags,
                                            profile=profile)

@std.route('/plan_report2/<int:selected_student_id>', methods=['GET', 'POST'])
@login_required
def plan_report2(selected_student_id):
    #print("In plan_report2 Request is :", request)
    std = student_select2(selected_student_id)

    return redirect(url_for('students.plan_report'))

##############END studets plan report###############	
			
	
##############START studets teachers###############	
	
@std.route('/edit_student_teachers', methods=['GET', 'POST'])
@login_required
def edit_student_teachers():
	
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('students.edit_students'))
	
	student_staff_teachers = get_student_teachers()
	#teachers_not_in_staff = get_teachers_not_of_student()	
	accupations = Accupation.query.filter(Accupation.hide == False).all()
	return render_template('./teachers/edit_student_teachers.html',   student=student, 
														   student_staff_teachers=student_staff_teachers,
														   accupations=accupations)
														   		
														  		
@std.route('/edit_student_teachers2/<int:selected_student_id>/<int:selected_teacher_id>', methods=['GET', 'POST'])
@login_required
def edit_student_teachers2(selected_student_id, selected_teacher_id):
	#print("In edit_student_teachers2 Request is :", request)
	std = student_select2(selected_student_id)
	if selected_teacher_id != 0:
		tchr = teacher_select2(selected_teacher_id)
	return edit_student_teachers()
 
 
@std.route('/teacher_to_student_add', methods=['GET', 'POST'])
@login_required
def teacher_to_student_add():

	#print("IN teacher_to_student_add")
	###########################impor pdb;pdb.set_trace()
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('teachers.student_select'))

	teachers_not_in_staff = get_teachers_not_of_student()

	accupations = Accupation.query.filter(Accupation.hide == False).all()
	if request.method == 'GET':
		return render_template('./teachers/edit_teachers_not_of_student.html', student=student, 
																	teachers_not_in_staff=teachers_not_in_staff,
																	accupations=accupations)
																																															
	teacher = Teacher.query.filter(Teacher.selected==True).first()
	if teacher == None:
		flash("Please select a teacher first ")
		return redirect(url_for('teachers.teacher_select'))
		
	exist_role = Role.query.filter(Role.student_id == student.id).filter(Role.teacher_id==teacher.id).count()
	sr = request.form.get('selected_role')
	#print("selected role is", sr)
	
	#print("exist_role:", exist_role)
	#print("exist_role:   role title:", exist_role, sr, request.method)
	
	if exist_role == 0:   #new Role
		###########################impor pdb;pdb.set_trace()
		role = Role(student.id, teacher.id, sr)
		role.teacher = teacher
		role.student = student
		student.teachers.append(role)			
		teacher.students.append(role)
		#print ("Role NEW title   NEW teacher    NEW student  :", role.title, role.teacher, role.student)

	else:
		role = Role.query.filter(Role.student_id == student.id).filter(Role.teacher_id==teacher.id).first()   #update role
		#print("Existing Role is", role)
		#print ("Role OLD title for student and teacher :", role.title, role.student_id, role.teacher_id)
		role.title=sr		
		#print ("Role NEW title   OLD teacher    OLD student  :", role.title, role.teacher, role.student)

	#print("IIIIIIIIIIIIIIIIIIIIIIn updating role ",  role.student.id, role.teacher_id, role.title)

	#DEBUG
	role = Role.query.filter(Role.teacher_id == teacher.id).filter(Role.student_id==student.id).first() 	
	#print("New Reole title is: Role student is   Role teacher is ", role.title, role.student, role.teacher)
	#DEBUG
	db.session.commit() 
	db.session.refresh(student)
	db.session.refresh(teacher)
	db.session.refresh(role)
	
	##print("teacher_to_student_add METHOD", request.method)
	return  redirect(url_for('students.edit_student_teachers')) 
		
		
	
@std.route('/teacher_to_student_add2/<int:selected_teacher_id>/<int:selected_student_id>', methods=['GET', 'POST'])
@login_required
def teacher_to_student_add2(selected_teacher_id, selected_student_id):
	#print(selected_student_id)
	student_select2(selected_student_id)
	##print(selected_teacher_id)
	if selected_teacher_id:
		teacher_select2(selected_teacher_id)
	return teacher_to_student_add()

		
@std.route('/teacher_from_student_delete', methods=['GET', 'POST'])
@login_required
def teacher_from_student_delete():
	###########################impor pdb;pdb.set_trace()
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('students.edit_students'))

	teacher = Teacher.query.filter(Teacher.selected==True).first()
	if teacher == None:
		flash("Please select a teacher first ")
		return redirect(url_for('select.teacher_select'))
		
	##print("SSSSSRRRRR IN student_from_teacher_delete   deleteing student %s from teacher %s :",student.id, teacher.id )			
	role = Role.query.filter(Role.student_id == student.id).filter(Role.teacher_id==teacher.id).first()   #update role
	if role:	
		###########################impor pdb;pdb.set_trace()
		#print ("deleting  ROLE  ", role.title)
		db.session.delete(role)
		db.session.commit()
	
	return  redirect(url_for('students.edit_student_teachers'))  #no change in students staff teachers
		
@std.route('/teacher_from_student_delete2/delete/<int:selected_teacher_id>/<int:selected_student_id>', methods=['GET', 'POST'])
@login_required
def teacher_from_student_delete2(selected_teacher_id, selected_student_id):
	##print("In DDDDDDDDDDDD student_from_teacher_delete2")
	std = student_select2(selected_student_id)
	if selected_teacher_id:
		##print(selected_teacher_id)
		tchr = teacher_select2(selected_teacher_id)
	return  redirect(url_for('students.teacher_from_student_delete'))  

	
	
@std.route('/get_student_teachers', methods=['GET', 'POST'])
@login_required
def get_student_teachers():
    student = Student.query.filter(Student.selected==True).first()
    if student == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))
        

    student_staff_teachers = Teacher.query.join(Role).filter(Role.student_id==student.id).filter(Role.teacher_id==Teacher.id).all()

    return student_staff_teachers


@std.route('/get_teachers_not_of_student', methods=['GET', 'POST'])
@login_required
def get_teachers_not_of_student():
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('students.edit_students'))
	
	#DEBUG
	###########################impor pdb;pdb.set_trace()	
	all_teachers = Teacher.query.all()

	student_staff_teachers = Teacher.query.join(Role).filter(Role.student_id==student.id).filter(Role.teacher_id==Teacher.id).all()
	
	teachers_with_no_students = Teacher.query.filter(~Teacher.students.any()).all()
	
	teachers_not_in_staff = list(set(all_teachers).difference(set(student_staff_teachers)))  #teachers_not_in_staff = all_teachers-student_staff_teachers
	
	teachers_not_in_staff.extend(teachers_with_no_students)

	###########################impor pdb;pdb.set_trace()
	#DEBUG

	return teachers_not_in_staff
##############studets teachers###############	


	
##############studets profiles###############	

@std.route('/edit_students_profile', methods=['GET', 'POST'])
@login_required
def edit_students_profile():
	###########################impor pdb;pdb.set_trace()
	#print("in edit_students_profile")
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('students.edit_students'))

	profile = Profile.query.filter(student.profile_id == Profile.id).first()
	if profile:
		return render_template('./profile/edit_students_profile.html', student=student, profile=profile)
															 
	else:
		return redirect(url_for('student.profile_to_student_add2', selected_student_id=student.id))

	return render_template('./profile/edit_students_profile.html', student=student, profile=profile)
														           
	
														  		
@std.route('/edit_students_profile2/<int:selected_student_id>', methods=['GET', 'POST'])
@login_required
def edit_students_profile2(selected_student_id):
	#print("In edit_students_profile2 Request is :", request)
	std = student_select2(selected_student_id)

	prf = Profile.query.filter(std.profile_id == Profile.id).first()
    
	if prf != None:
		prf = profile_select2(prf.id)
	else:
		return profile_to_student_add()
        
	return edit_students_profile()
 
@std.route('/profile_to_student_add', methods=['GET', 'POST'])
@login_required
def profile_to_student_add():
    #print("In profile_to_student_add")
    user = User.query.get_or_404(current_user._get_current_object().id)
    author_id = user.id
        
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('edit_students'))

    #get data from form and insert to postgress db
    title = request.form.get("profle for std.first_name + std.last_name student")
    body = request.form.get("profle for std.first_name + std.last_name student")

    ###########################impor pdb;pdb.set_trace() 	
    prf = Profile(title, body)	 #Create a new profile 
    prf = profile_select2(prf.id)            # select the new created profile
    student.profile_id = prf.id

       
    db.session.add(profile) 	
    db.session.commit()  
    db.session.refresh(profile)

    #print("In profile_to_student_add", student.id, prf.id)

    url = url_for('students.edit_students_profile', selected_student_id=student.id )
    return redirect(url)   

@std.route('/profile_to_student_add2/add/<int:selected_student_id>', methods=['GET', 'POST'])
@login_required
def profile_to_student_add2(selected_student_id):
    ##print("In DDDDDDDDDDDD profile_from_student_delete2")
    std = student_select2(selected_student_id)
    return redirect(url_for('students.profile_to_student_add'))  

	
@std.route('/profile_from_student_delete', methods=['GET', 'POST'])
@login_required
def profile_from_student_delete():
	###########################impor pdb;pdb.set_trace()
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('students.edit_students'))

	profile = Profile.query.filter(Profile.selected==True).first()
	if profile == None:
		flash("Please select a profile first ")
		return redirect(url_for('select.profile_select'))
	
	##print("SSSSSRRRRR IN profile_from_student_delete   deleteing student %s from profile %s :",student.id, profile.id )			

	#print("deleteint profile from student %s ", profile.title)		
	db.session.delete(profile)		
	db.session.commit() 
	
	return  redirect(url_for('students.edit_students_profile'))  #no change in students staff profiles
		
@std.route('/profile_from_student_delete2/delete/<int:selected_student_id>/<int:selected_profile_id>', methods=['GET', 'POST'])
@login_required
def profile_from_student_delete2(selected_student_id, selected_profile_id):
	##print("In DDDDDDDDDDDD profile_from_student_delete2")
	std = student_select2(selected_student_id)
	if selected_profile_id:
		##print(selected_profile_id)
		prf = profile_select2(selected_profile_id)
	return  redirect(url_for('students.profile_from_student_delete'))  

	
	
@std.route('/get_students_profile', methods=['GET', 'POST'])
@login_required
def get_students_profile():
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('students.edit_students'))

	profile = Profile.query.join(Student.pros).filter(Student.id==student.id)	
	return profile


##############studets profile subj


@std.route('/edit_std_profile_subjects', methods=['GET', 'POST'])
@login_required
def edit_std_profile_subjects():

    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('index'))
	
    profile = Profile.query.filter(Profile.selected==True).first()
    print("in subjectes_by_profile profile selected is")
    print(profile.title)
    if profile == None:
        flash("Please select an profile first ")
        return redirect(url_for('profile_select'))

    std_subjects = Subject.query.filter(std.profile_id == profile.id).all()
    #############import_pdb; pdb.set_trace()
    subjectes = Subject.query.join(Profile.subjects).filter(Profile.id==profile.id)
    
    return render_template('./profile/edit_students_profile.html',
                            student=std,
                            profile=profile,
                            subjectes=std_subjects
							)


	
@std.route('/match_subject_to_std_profile', methods=['GET', 'POST'])
@login_required
def match_subject_to_std_profile():
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))		

    sbj = Subject.query.filter(Subject.selected==True).first()	
    if sbj == None:
        flash("Please select a subject to add first ")
        return redirect(url_for('subjectes.edit_subjectes'))

    profile = Profile.query.filter(Profile.selected==True).first()	
    if profile == None:
        flash("Please select a profile  first ")
        return redirect(url_for('subjectes.edit_studnets'))

    ############impor pdb;pdb.set_trace()
    print("IN match_subject_to_std_profile", profile, std, sbj)
    ##################import_pdb; pdb.set_trace()
           
    profile.subjects.append(sbj)	

    db.session.add(sbj)    
    db.session.commit()  
    db.session.refresh(sbj)

    sbj.selected=False
    return redirect(url_for('students.edit_students_profile'))
			
@std.route('/match_subject_to_std_profile2/<int:selected_subject_id>', methods=['GET', 'POST'])
@login_required
def match_subject_to_std_profile2(selected_subject_id):
    ###########import_pdb;pdb.set_trace()
    sbj = subject_select2(selected_subject_id)
    return redirect(url_for('students.match_subject_to_std_profile')) 	

            
@std.route('/subject_to_std_profile_add', methods=['GET', 'POST'])
@login_required
def subject_to_std_profile_add():

    ###########import_pdb; pdb.set_trace()
    
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))		
 
    profile = Profile.query.filter(Profile.selected==True).first()
    if profile == None:
        flash("Please select a profile first ")
        return redirect(url_for('students.edit_students'))		

    ###########import_pdb; pdb.set_trace()
    all_subjects = Subject.query.all()
    subjects_not_of_student = list(set(all_subjects).difference(set(profile.subjects)))  #subjects_not_of_student = all_subjects-student's subjects

    ############################impor pdb;pdb.set_trace()
    if request.method == 'GET':
        return render_template('./profile/edit_subjects_not_of_std2.html',
                                                                student=std,
                                                                profile=profile,
                                                                subjects=subjects_not_of_student) 
                                                                

@std.route('/subject_to_std_profile_add2/<int:selected_student_id>', methods=['GET', 'POST'])
@login_required
def subject_to_std_profile_add2(selected_student_id):
	###########################impor pdb;pdb.set_trace()
	std = student_select2(selected_student_id)
	#dest = subject_select2(selected_subject_id)
	return redirect(url_for('students.subject_to_std_profile_add')) 	
	
	
@std.route('/subject_from_std_profile_delete', methods=['GET', 'POST'])
@login_required
def subject_from_std_profile_delete():
	
    profile = Profile.query.filter(Profile.selected==True).first()	
    if profile == None:
        flash("Please select a profile  first ")
        return redirect(url_for('subjectes.edit_studnets'))

    sbj = Subject.query.filter(Subject.selected==True).first()
    if sbj == None:
        flash("Please select a subject to delete first ")
        return redirect(url_for('subjectes.edit_subjectes'))
            
    print ("DDDDDDDDDDDDDD In subject_from_student_delete deleting  profile subject ", profile, sbj )

    profile.subjects.remove(sbj)

    db.session.commit()  

    return redirect(url_for('students.edit_students_profile')) 

@std.route('/subject_from_std_profile_delete2/<int:selected_subject_id>', methods=['GET', 'POST'])
@login_required
def subject_from_std_profile_delete2(selected_subject_id):
	sbj = subject_select2(selected_subject_id)
	return redirect(url_for('students.subject_from_std_profile_delete')) 	

##############studets profile subj


##############studets profile wkns


@std.route('/edit_std_profile_weaknesses', methods=['GET', 'POST'])
@login_required
def edit_std_profile_weaknesses():

    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('index'))
	
    profile = Profile.query.filter(Profile.selected==True).first()
    print("in weaknesses_by_profile profile selected is")
    print(profile.title)
    if profile == None:
        flash("Please select an profile first ")
        return redirect(url_for('profile_select'))

    std_weaknesses = Weakness.query.filter(std.profile_id == profile.id).all()
    #############import_pdb; pdb.set_trace()
    weaknesses = Weakness.query.join(Profile.weaknesses).filter(Profile.id==profile.id)
    
    return render_template('./profile/edit_students_profile.html',
                            student=std,
                            profile=profile,
                            weaknesses=std_weaknesses
							)


	
@std.route('/match_weakness_to_std_profile', methods=['GET', 'POST'])
@login_required
def match_weakness_to_std_profile():
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))		

    wkns = Weakness.query.filter(Weakness.selected==True).first()	
    if wkns == None:
        flash("Please select a weakness to add first ")
        return redirect(url_for('weaknesses.edit_weaknesses'))

    profile = Profile.query.filter(Profile.selected==True).first()	
    if profile == None:
        flash("Please select a profile  first ")
        return redirect(url_for('weaknesses.edit_studnets'))

    ############impor pdb;pdb.set_trace()
    print("IN match_weakness_to_std_profile", profile, std, wkns)
    ##################import_pdb; pdb.set_trace()
           
    profile.weaknesses.append(wkns)	

    db.session.add(wkns)    
    db.session.commit()  
    db.session.refresh(wkns)

    wkns.selected=False
    return redirect(url_for('students.edit_students_profile'))
			
@std.route('/match_weakness_to_std_profile2/<int:selected_weakness_id>', methods=['GET', 'POST'])
@login_required
def match_weakness_to_std_profile2(selected_weakness_id):
    ###########import_pdb;pdb.set_trace()
    wkns = weakness_select2(selected_weakness_id)
    return redirect(url_for('students.match_weakness_to_std_profile')) 	

            
@std.route('/weakness_to_std_profile_add', methods=['GET', 'POST'])
@login_required
def weakness_to_std_profile_add():

    ###########import_pdb; pdb.set_trace()
    
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))		
 
    profile = Profile.query.filter(Profile.selected==True).first()
    if profile == None:
        flash("Please select a profile first ")
        return redirect(url_for('students.edit_students'))		

    ###########import_pdb; pdb.set_trace()
    all_weaknesses = Weakness.query.all()
    weaknesses_not_of_student = list(set(all_weaknesses).difference(set(profile.weaknesses)))  #weaknesses_not_of_student = all_weaknesses-student's weaknesses

    ############################impor pdb;pdb.set_trace()
    if request.method == 'GET':
        return render_template('./profile/edit_weaknesses_not_of_std2.html',
                                                                student=std,
                                                                profile=profile,
                                                                weaknesses=weaknesses_not_of_student) 
                                                                

@std.route('/weakness_to_std_profile_add2/<int:selected_student_id>', methods=['GET', 'POST'])
@login_required
def weakness_to_std_profile_add2(selected_student_id):
	###########################impor pdb;pdb.set_trace()
	std = student_select2(selected_student_id)
	#dest = weakness_select2(selected_weakness_id)
	return redirect(url_for('students.weakness_to_std_profile_add')) 	
	
	
@std.route('/weakness_from_std_profile_delete', methods=['GET', 'POST'])
@login_required
def weakness_from_std_profile_delete():
	
    profile = Profile.query.filter(Profile.selected==True).first()	
    if profile == None:
        flash("Please select a profile  first ")
        return redirect(url_for('weaknesses.edit_studnets'))

    wkns = Weakness.query.filter(Weakness.selected==True).first()
    if wkns == None:
        flash("Please select a weakness to delete first ")
        return redirect(url_for('weaknesses.edit_weaknesses'))
            
    print ("DDDDDDDDDDDDDD In weakness_from_student_delete deleting  profile weakness ", profile, wkns )

    profile.weaknesses.remove(wkns)

    db.session.commit()  

    return redirect(url_for('students.edit_students_profile')) 

@std.route('/weakness_from_std_profile_delete2/<int:selected_weakness_id>', methods=['GET', 'POST'])
@login_required
def weakness_from_std_profile_delete2(selected_weakness_id):
	wkns = weakness_select2(selected_weakness_id)
	return redirect(url_for('students.weakness_from_std_profile_delete')) 	

##############studets profile wkns


##############studets profile strn

@std.route('/edit_std_profile_strengthes', methods=['GET', 'POST'])
@login_required
def edit_std_profile_strengthes():

    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('index'))
	
    profile = Profile.query.filter(Profile.selected==True).first()
    print("in strengthes_by_profile profile selected is")
    print(profile.title)
    if profile == None:
        flash("Please select an profile first ")
        return redirect(url_for('profile_select'))

    std_strengthes = Strength.query.filter(std.profile_id == profile.id).all()
    #############import_pdb; pdb.set_trace()
    strengthes = Strength.query.join(Profile.strengthes).filter(Profile.id==profile.id)
    
    return render_template('./profile/edit_students_profile.html',
                            student=std,
                            profile=profile,
                            strengthes=std_strengthes
							)


	
@std.route('/match_strength_to_std_profile', methods=['GET', 'POST'])
@login_required
def match_strength_to_std_profile():
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))		

    strn = Strength.query.filter(Strength.selected==True).first()	
    if strn == None:
        flash("Please select a strength to add first ")
        return redirect(url_for('students.edit_students_profile'))

    profile = Profile.query.filter(Profile.selected==True).first()	
    if profile == None:
        flash("Please select a profile  first ")
        return redirect(url_for('strengthes.edit_studnets'))

    ############impor pdb;pdb.set_trace()
    print("IN match_strength_to_std_profile", profile, std, strn)
    ##################import_pdb; pdb.set_trace()
           
    profile.strengthes.append(strn)	

    db.session.add(strn)    
    db.session.commit()  
    db.session.refresh(strn)

    strn.selected=False
    return redirect(url_for('students.edit_students_profile'))
			
@std.route('/match_strength_to_std_profile2/<int:selected_strength_id>', methods=['GET', 'POST'])
@login_required
def match_strength_to_std_profile2(selected_strength_id):
    ###########import_pdb;pdb.set_trace()
    strn = strength_select2(selected_strength_id)
    return redirect(url_for('students.match_strength_to_std_profile')) 	

            
@std.route('/strength_to_std_profile_add', methods=['GET', 'POST'])
@login_required
def strength_to_std_profile_add():

    ###########import_pdb; pdb.set_trace()
    
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))		
 
    profile = Profile.query.filter(Profile.selected==True).first()
    if profile == None:
        flash("Please select a profile first ")
        return redirect(url_for('students.edit_students'))		

    ###########import_pdb; pdb.set_trace()
    all_strengthes = Strength.query.all()
    strengthes_not_of_student = list(set(all_strengthes).difference(set(profile.strengthes)))  #strengthes_not_of_student = all_strengthes-student's strengthes

    ############################impor pdb;pdb.set_trace()
    if request.method == 'GET':
        return render_template('./profile/edit_strengthes_not_of_std2.html',
                                                                student=std,
                                                                profile=profile,
                                                                strengthes=strengthes_not_of_student) 
                                                                

@std.route('/strength_to_std_profile_add2/<int:selected_student_id>', methods=['GET', 'POST'])
@login_required
def strength_to_std_profile_add2(selected_student_id):
	###########################impor pdb;pdb.set_trace()
	std = student_select2(selected_student_id)
	#dest = strength_select2(selected_strength_id)
	return redirect(url_for('students.strength_to_std_profile_add')) 	
	
	
@std.route('/strength_from_std_profile_delete', methods=['GET', 'POST'])
@login_required
def strength_from_std_profile_delete():
	
    profile = Profile.query.filter(Profile.selected==True).first()	
    if profile == None:
        flash("Please select a profile  first ")
        return redirect(url_for('strengthes.edit_studnets'))

    strn = Strength.query.filter(Strength.selected==True).first()
    if strn == None:
        flash("Please select a strength to delete first ")
        return redirect(url_for('students.edit_students_profile'))

    print ("DDDDDDDDDDDDDD In strength_from_student_delete deleting  profile strength ", profile, strn )

    profile.strengthes.remove(strn)

    db.session.commit()  

    return redirect(url_for('students.edit_students_profile')) 

@std.route('/strength_from_std_profile_delete2/<int:selected_strength_id>', methods=['GET', 'POST'])
@login_required
def strength_from_std_profile_delete2(selected_strength_id):
	strn = strength_select2(selected_strength_id)
	return redirect(url_for('students.strength_from_std_profile_delete')) 	

##############studets profile strn

##############studets profiles###############	


##############studets destinations###############	
@std.route('/edit_student_destinations', methods=['GET', 'POST'])
@login_required
def edit_student_destinations():
    #######################impor pdb;pdb.set_trace()
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))
                                
    ###########################impor pdb;pdb.set_trace()
    std_age_range = get_student_default_age_range(std.birth_date)
    
    all_tags = Tag.query.all() 
        
    #DEBUG
    std_dst_ids = []
    for st in std.destinations:
        std_dst_ids.append(st.destination_id)
    #print("111111111 std_dst_ids: ", std_dst_ids)
    ##################import_pdb; pdb.set_trace()
    ########################impor pdb;pdb.set_trace()
    return render_template('./destinations/edit_std_dst_by_tag.html', 
                                                            std = std, 
                                                            tags=all_tags,
                                                            std_dst_ids=std_dst_ids)
                                                               
                                                                
                                                                

																												  		
@std.route('/edit_student_destinations2/edit/<int:selected_student_id>/<int:selected_destination_id>', methods=['GET', 'POST'])
@login_required
def edit_student_destinations2(selected_student_id, selected_destination_id):
	#print("In edit_student_destinations2 Request is :", request)
	std = student_select2(selected_student_id)
	if selected_destination_id != 0:
		dest = destination_select2(selected_destination_id)
	return redirect(url_for('students.edit_student_destinations'))		


@std.route('/update_student_age_range_for_edit_destination/edit/<int:selected_student_id>', methods=['GET', 'POST'])
@login_required
def update_student_age_range_for_edit_destination(selected_student_id):
    #print("In edit_student_destinations2 Request is :", request)
    std = student_select2(selected_student_id)
    student = Student.query.filter(Student.selected==True).first()

    ar_title = request.form.get('selected_age_range')
    ar = Age_range.query.filter(Age_range.title == ar_title).first()
    age_ranges = Age_range.query.all();
    return render_template('./destinations/edit_student_destinations.html', student=student, age_ranges=age_ranges, default_age_range = ar)

@std.route('/update_student_scrt_for_edit_destination/edit/<int:selected_student_id>', methods=['GET', 'POST'])
@login_required
def update_student_scrt_for_edit_destination(selected_student_id):
    #print("In update_student_ scrt_ for_edit_destination Request is :", request)
    std = student_select2(selected_student_id)
    student = Student.query.filter(Student.selected==True).first()

    ar_title = request.form.get('selected_age_range')
    ar = Age_range.query.filter(Age_range.title == ar_title).first()
    age_ranges = Age_range.query.all();
    return render_template('edit_student_destinations.html', student=student, age_ranges=age_ranges, default_age_range = ar)


@std.route('/get_student_default_age_range/<string:birth_date>', methods=['GET', 'POST'])
@login_required
def get_student_default_age_range(birth_date):
    today = date.today()
    age = today.year - birth_date.year
    full_year_passed = (today.month, today.day) < (birth_date.month, birth_date.day)
    if not full_year_passed:
        age -= 1
    age_ranges = Age_range.query.all()
    for ar in age_ranges:
        if ar in range(ar.from_age ,ar.to_age):
            return ar
    if age < 3:
        ar = Age_range.query.filter(Age_range.to_age < 6).first()
    else:  
        ar = Age_range.query.filter(Age_range.from_age > 17).first()
    return ar
            
            
@std.route('/destination_to_student_add', methods=['GET', 'POST'])
@login_required
def destination_to_student_add():
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))		
 
    
    std_dst_ids = []
    for st in std.destinations:
        std_dst_ids.append(st.destination_id)
    
    ##################import_pdb; pdb.set_trace()
    destinations_of_std_and_dummy = Std_destination.query.filter(Std_destination.student_id==0).filter(Std_destination.destination_id.in_(std_dst_ids)).all()
    all_destinations = Std_destination.query.filter(Std_destination.student_id==0).all()   # Humpty dumpty has id=0 and all destinations 
    destinations_not_of_student = list(set(all_destinations).difference(set(destinations_of_std_and_dummy)))  #destinations_not_of_student = all_destinations-student's destinations

    age_ranges = Age_range.query.all()
    tags = Tag.query.all() 
    ############################impor pdb;pdb.set_trace()
    if request.method == 'GET':
        return render_template('./destinations/edit_destinations_not_of_student.html',
                                                                std=std,
                                                                destinations=destinations_not_of_student, 
                                                                age_ranges=age_ranges,
                                                                tags=tags)

@std.route('/destination_to_student_add2/<int:selected_student_id>', methods=['GET', 'POST'])
@login_required
def destination_to_student_add2(selected_student_id):
	###########################impor pdb;pdb.set_trace()
	std = student_select2(selected_student_id)
	#dest = destination_select2(selected_destination_id)
	return redirect(url_for('students.destination_to_student_add')) 	
	
	
@std.route('/match_destination_to_student', methods=['GET', 'POST'])
@login_required
def match_destination_to_student():
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))		

    dst = Destination.query.filter(Destination.selected==True).first()	
    if dst == None:
        flash("Please select a destination to add first ")
        return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=0))

    ############impor pdb;pdb.set_trace()
    print("IN match_destination_to_student", std, dst)
    ##################import_pdb; pdb.set_trace()
    
    std_dst = Std_destination(std.id, dst.id)
    std_dst.student = std
    std_dst.destination = dst
    std.destinations.append(std_dst)
    dst.students.append(std_dst)

    for tag in dst.tags:
        std_tag = Std_tag.query.filter(Std_tag.student_id==std.id).filter(Std_tag.tag_id==tag.tag_id).first()
        if std_tag == None:
            std_tag = Std_tag(std.id, tag.tag_id)
            std_tag.student = std
            std_tag.tag = tag.tag            
            std.tags.append(std_tag)
            tag.tag.students.append(std_tag)
                    
    dst.selected=False
    
    db.session.commit() 
    
    return redirect(url_for('students.edit_student_destinations'))
			
@std.route('/match_destination_to_student2/<int:selected_destination_id>', methods=['GET', 'POST'])
@login_required
def match_destination_to_student2(selected_destination_id):
    #########################impor pdb;pdb.set_trace()
    dest = destination_select2(selected_destination_id)
    return redirect(url_for('students.match_destination_to_student')) 	


@std.route('/destination_from_student_delete', methods=['GET', 'POST'])
@login_required
def destination_from_student_delete():
	
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('students.edit_students'))		

	destination = Destination.query.filter(Destination.selected==True).first()
	if destination == None:
		flash("Please select a destination to delete first ")
		return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=0))
			
	#print ("delete selected destination is " )
	#print(destination.title)      
	
	student.destinations.remove(destination)
	db.session.commit()  

	return redirect(url_for('students.edit_student_destinations')) 

@std.route('/destination_from_student_delete2/<int:selected_student_id><int:selected_destination_id>', methods=['GET', 'POST'])
@login_required
def destination_from_student_delete2(selected_student_id, selected_destination_id):
	std = student_select2(selected_student_id)
	dest = destination_select2(selected_destination_id)
	return redirect(url_for('students.destination_from_student_delete')) 	

##############studets destinations###############	

	
##############START studets goals###############	
	
@std.route('/edit_student_goals', methods=['GET', 'POST'])
@login_required
def edit_student_goals():

    
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))

    dst = Destination.query.filter(Destination.selected==True).first()
    #print("IN edit_student_goals dst is: ", dst)
    if dst == None:
        flash("Please select a destination first ")
        return redirect(url_for('students.edit_student_destinations'))
    ############impor pdb;pdb.set_trace()
    
    student_goals = Std_goal.query.filter(Std_goal.student_id==std.id).filter(Std_goal.dst_id==dst.id).all()
    statuss = Status.query.all()
    whos = Accupation.query.all()
  
    student_todos = Std_todo.query.filter(Std_todo.student_id==std.id).filter(Std_todo.dst_id==dst.id).all()

    statuss = Status.query.all()
    whos = Accupation.query.all()

    todos_not_of_student = get_dst_todos_not_of_student()
    due_date = date.today()
                
    return render_template('./goals/edit_std_dst_goals.html', std=std, dst=dst, 
                                                              std_goals=student_goals, student_todos=student_todos,
                                                              todos_not_of_student = todos_not_of_student,
                                                              statuss=statuss, whos=whos, due_date=due_date)
                                                                
														  		
@std.route('/edit_student_goals2/<int:selected_student_id>/<int:selected_destination_id>', methods=['GET', 'POST'])
@login_required
def edit_student_goals2(selected_student_id, selected_destination_id):

    std = student_select2(selected_student_id)
    dst = destination_select2(selected_destination_id)
    #print("In edit_student_goals2 std dst :", std, dst.id)

    return edit_student_goals()
    
		
@std.route('/goal_from_student_delete', methods=['GET', 'POST'])
@login_required
def goal_from_student_delete():
	###########################impor pdb;pdb.set_trace()
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('students.edit_students'))

	goal = Goal.query.filter(Goal.selected==True).first()
	if goal == None:
		flash("Please select a goal first ")
		return redirect(url_for('select.goal_select'))
		
	##print("SSSSSRRRRR IN student_from_goal_delete   deleteing student %s from goal %s :",student.id, goal.id )			
	std_goal = Std_goal.query.filter(Std_goal.student_id == student.id).filter(Std_goal.goal_id==goal.id).first()   #update std_goal
	if std_goal:	
		###########################impor pdb;pdb.set_trace()
		#print ("deleting  ROLE  ", std_goal.title)
		db.session.delete(std_goal)
		db.session.commit()
	
	return  redirect(url_for('students.edit_student_goals'))  #no change in students staff goals
		
@std.route('/goal_from_student_delete2/delete/<int:selected_goal_id>/<int:selected_student_id>', methods=['GET', 'POST'])
@login_required
def goal_from_student_delete2(selected_goal_id, selected_student_id):
	##print("In DDDDDDDDDDDD student_from_goal_delete2")
	std = student_select2(selected_student_id)
	if selected_goal_id:
		##print(selected_goal_id)
		tchr = goal_select2(selected_goal_id)
	return  redirect(url_for('students.goal_from_student_delete'))  

##############studets goals###############		


	
##############START TRY studets goals###############	

@std.route('/try_goal_to_student_add', methods=['GET'])
@login_required
def try_goal_to_student_add():
    ########impor pdb;pdb.set_trace()
    #print("IN goal_to_student_add")
    ###########################impor pdb;pdb.set_trace()
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('destination.edit_students'))

    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_student_destinations'))		

    #print("IN try_goal_to_student_add Request methi", request.method)
    ########impor pdb;pdb.set_trace()
    #### GET case
            
    goals_not_of_student = try_get_goals_not_of_student()
    if len(goals_not_of_student) < 1:
        flash("כל היעדים של מטרה זו כבר משוייכים לתלמיד. אפשר ליצור יעד חדש דרך  עריכת יעדים למטרה  ")
        ########impor pdb;pdb.set_trace()
        redirect(url_for('students.edit_student_goals'))

    statuss = Status.query.all()
    due_date = date.today()
    
    student_goals = Std_goal.query.filter(Std_goal.student_id==std.id).filter(Std_goal.dst_id==dst.id).all()
 
    
    return render_template('./goals/edit_std_goals_and_std_not_of_std_goals.html', std=std, dst=dst, 
                                                                goals_not_of_student=goals_not_of_student,
                                                                statuss=statuss, due_date=due_date,
                                                                std_goals=student_goals)
	                           
   
##############START match_goal_to_std ###############	

@std.route('/match_goal_to_std', methods=['POST'])
@login_required
def match_goal_to_std():

    ###############import pdb;;;;;pdb.set_trace()
    print("IN goal_to_student_add")
    ###########################impor pdb;pdb.set_trace()
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('destination.edit_students'))

    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_student_destinations'))		
   
    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('students.edit_student_goals'))

    statuss = Status.query.all()
    
    print(" std dst goal ", std, dst, goal )

    std_goal = Std_goal.query.filter(Std_goal.student_id == std.id).filter(Std_goal.goal_id==goal.id).first()
    new_std = False
    if std_goal == None:   #new Std_goal
        new_std = True
        std_goal = Std_goal(std.id, goal.id)        

    std_goal.goal_title = goal.title
    std_goal.goal_body = goal.body
    
    std_goal.goal = goal
    std_goal.student = std    
    std_goal.dst_id = dst.id
    
    ########import_pdb;pdb.set_trace()
    
    sts_title = request.form.get('selected_status')
    sts = Status.query.filter(Status.title==sts_title).first() 
    std_goal.status_id = sts.id
    std_goal.status_title = sts.title
    std_goal.status_color = sts.color
    print("selected sts is  sts-color ts-title: ", sts, sts.color, sts.title)   
    
    std_goal.due_date = request.form.get('due_date') 
    
    if new_std:
        std.goals.append(std_goal)			
        goal.students.append(std_goal)
          
    print("goal is  for std is : Std_goal student is  ", std_goal, std)
    
    goal.selected = False
    #DEBUG
    db.session.commit() 
    db.session.refresh(std)
    db.session.refresh(goal)
    db.session.refresh(std_goal)

    ##print("goal_to_student_add METHOD", request.method)
    return  redirect(url_for('students.edit_student_goals')) 
        
		
	
@std.route('/match_goal_to_std2/<int:selected_goal_id>', methods=['GET', 'POST'])
@login_required
def match_goal_to_std2(selected_goal_id):

    print("IN match_goal_to_std2   goal ", selected_goal_id)
    
    ###import_pdb; pdb.set_trace()
    goal = goal_select2(selected_goal_id)
    
    return match_goal_to_std()
    
##############END match_goal_to_std ###############	


################## START update_std_goal_form ################    
@std.route('/update_std_goal_form', methods=['GET', 'POST'])
@login_required
def update_std_goal_form():

    ###impor pdb; pdb.set_trace()
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('destination.edit_students'))

    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_student_destinations'))		
   
    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('students.edit_student_goals'))
            
    updated_std_goal = Std_goal.query.filter(Std_goal.selected==True).first()
    if updated_std_goal == None:
        flash("Please select a student's goal to update")
        return redirect(url_for('students.edit_student_goals'))
        
    ##impor pdb; pdb.set_trace()
    
    if updated_std_goal == None:   #Add a new Std_goal
        updated_std_goal = Std_goal(std.id, goal.id)
        std_goal = std_goal_select2(selected_goal_id, std.id) 
        updated_std_goal.goal_title = request.form.get('goal_id')
        updated_std_goal.goal_body =  request.form.get('goal_body')    
        updated_std_goal.goal = goal
        updated_std_goal.student = std    
        updated_std_goal.dst_id = dst.id
        std.goals.append(updated_std_goal)			
        goal.students.append(updated_std_goal)
        
    status = Status.query.filter(Status.id==request.form['status']).first()    
    #print("selected sts is status", status,status.id, status.title, status.color )   
    updated_std_goal.status_id = status.id
    updated_std_goal.status_title = status.title
    updated_std_goal.status_color = status.color
    
    updated_std_goal.due_date = request.form.get('due_date') 
           
    print ("In update_std_goal_form NEW std_goal: goal student date  sts:",  updated_std_goal.goal, updated_std_goal.student, updated_std_goal.due_date, updated_std_goal.status_title)
    #DEBUG
    #print("New goal is  for std is : Std_goal student is  ", updated_std_goal, std)
    goal.selected = False
    updated_std_goal.selected = False
    #DEBUG
    db.session.commit() 

    ##print("goal_to_student_add METHOD", request.method)
    return  redirect(url_for('students.edit_student_goals')) 


@std.route('/update_std_goal_form2', methods=['GET', 'POST'])
@login_required
def update_std_goal_form2():
    ##impor pdb; pdb.set_trace()
    selected_goal_id = request.form['goal_id']
    
    goal = goal_select2(selected_goal_id) 
    #print("In UUUUUUUUUU update_std_goal_form2 selected goal_id ", goal.id)
    
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('destination.edit_students'))

    std_goal = std_goal_select2(goal.id, std.id) 

    return update_std_goal_form()			

############################### END update_std_goal_form
                                            
                                            
@std.route('/try_get_student_goals', methods=['GET', 'POST'])
@login_required
def try_get_student_goals():
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))
        
    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_student_destinations'))		
        

    student_goals = Goal.query.join(Std_goal).filter(Std_goal.dst_id==dst.id).filter(Std_goal.student_id==std.id).all()

    return student_goals


@std.route('/try_get_goals_not_of_student', methods=['GET', 'POST'])
@login_required
def try_get_goals_not_of_student():
    student = Student.query.filter(Student.selected==True).first()
    if student == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))
        
    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_student_destinations'))		

    #DEBUG
    ###########################impor pdb;pdb.set_trace()	
    all_dst_goals = Goal.query.join(Destination).filter(Goal.dst_id == dst.id)

    student_goals = Goal.query.join(Std_goal).filter(Std_goal.student_id==student.id).filter(Std_goal.goal_id==Goal.id).all()

    goals_with_no_students = Goal.query.filter(~Goal.students.any()).all()

    goals_not_of_student = list(set(all_dst_goals).difference(set(student_goals)))  #goals_not_of_student = all_dst_goals-student_goals

    goals_not_of_student.extend(goals_with_no_students)

    return goals_not_of_student


		
@std.route('/goal_from_student_delete', methods=['GET', 'POST'])
@login_required
def std_goal_delete():

    std_goal = Std_goal.query.filter(Std_goal.selected==True).first()
    if std_goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('students.edit_student_goals'))

    db.session.delete(std_goal)
    db.session.commit()

    return  redirect(url_for('students.edit_student_goals'))  #no change in students staff goals
        
@std.route('/std_goal_delete2/delete/<int:selected_std_id>/<int:selected_goal_id>', methods=['GET', 'POST'])
@login_required
def std_goal_delete2(selected_std_id, selected_goal_id):

    std_goal = std_goal_select2(selected_std_id, selected_goal_id)
    return  redirect(url_for('students.std_goal_delete'))  
        
        
############## END TRY studets goals###############



############# START STD TODOS #############################
	
@std.route('/edit_student_todos', methods=['GET', 'POST'])
@login_required
def edit_student_todos():
    ##############import_pdb; pdb.set_trace()
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a goal first ")
        return redirect(url_for('students.edit_students'))		
    
    std_goal = Std_goal.query.filter(Std_goal.selected==True).first()
    if std_goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('students.edit_student_goals'))	
        
    dst = Destination.query.filter(Destination.id==std_goal.dst_id).first()
    if dst == None:
        flash("Please select a destination for student first ")
        return redirect(url_for('students.edit_student_destinations'))		
   
    print(" IN edit_student_todos std std_dst  std_goals ",  std, dst, std_goal)
    ##############import_pdb; pdb.set_trace()
    
    student_todos = Std_todo.query.filter(Std_todo.student_id==std_goal.student_id).filter(Std_todo.goal_id==std_goal.goal_id).all()
    
    print(" student_todos", student_todos)
    ###import_pdb; psb.set_trace()
    
    for st in student_todos:
        todo=Todo.query.filter(Todo.id==st.todo_id).first()
        if todo.title !=None:
            st.todo_title = todo.title
        if todo.body != None:
            st.todo_body = todo.body
            
    statuss = Status.query.all()
    whos = Accupation.query.all()    

    return render_template('./goals/todos/edit_std_todos.html', std=std, dst=dst, std_goal=std_goal, 
                                                                std_todos=student_todos,statuss=statuss, whos=whos)

														  		
@std.route('/edit_student_todos2/<int:selected_std_id>/<int:selected_goal_id>', methods=['GET', 'POST'])
@login_required
def edit_student_todos2(selected_std_id, selected_goal_id):
    #################import_pdb; pdb.set_trace()
    std_goal = std_goal_select2(selected_std_id, selected_goal_id)

    return edit_student_todos()

														  		
@std.route('/get_std_todos', methods=['GET', 'POST'])
@login_required
def get_std_todos(std, std_goal, dst):
    #############################import_pdb; pdb.set_trace()
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a goal first ")
        return redirect(url_for('students.edit_students'))		
    
    std_goal = Std_goal.query.filter(Std_goal.selected==True).first()
    if std_goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('students.edit_student_goals'))	
        
    dst = Destination.query.filter(Destination.id==std_goal.dst_id).first()
    if dst == None:
        flash("Please select a destination for student first ")
        return redirect(url_for('students.edit_student_destinations'))		
   
    print(" IN edit_student_todos std std_dst  std_goals ",  std, dst, std_goal)
    ############################import_pdb; pdb.set_trace()
    
    student_todos = Std_todo.query.filter(Std_todo.student_id==std_goal.student_id).filter(Std_todo.goal_id==std_goal.goal_id).all()

    for st in student_todos:
        todo=Todo.query.filter(Todo.id==st.todo_id).first()
        if todo.title !=None:
            st.todo_title = todo.title
        if todo.body != None:
            st.todo_body = todo.body
    
    return student_todos      

	
##############START TRY studets todos###############	

@std.route('/try_todo_to_student_add', methods=['GET'])
@login_required
def try_todo_to_student_add():
    ########impor pdb;pdb.set_trace()
    #print("IN todo_to_student_add")
    ###########################impor pdb;pdb.set_trace()
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('destination.edit_students'))

    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_student_destinations'))		

    std_goal = Std_goal.query.filter(Std_goal.selected==True).first()
    if std_goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('students.edit_student_goals'))		

    #print("IN try_todo_to_student_add Request methi", request.method)
    #### GET case
    todos_not_of_student = get_todos_not_of_student()
    
    ###############################import_pdb; pdb.set_trace()
    
    if (todos_not_of_student == None) or (len(todos_not_of_student) < 1):
        flash("כל המשימות של יעדזה כבר משוייכות לתלמיד. אפשר ליצור משימה חדשה דרך יצירת מטרות-יעדים-משימות.")
        ########impor pdb;pdb.set_trace()
        redirect(url_for('students.edit_student_todos'))

    statuss = Status.query.all()
    whos = Accupation.query.all()
    due_date = date.today()
    return render_template('./goals/todos/edit_todos_not_of_std.html', std=std, dst=dst, std_goal=std_goal,
                                                                todos_not_of_student=todos_not_of_student,
                                                                statuss=statuss, whos=whos, due_date=due_date)
	
##############START match_todo_to_std ###############	

@std.route('/match_todo_to_std', methods=['GET', 'POST'])
@login_required
def match_todo_to_std():

    print("IN match_todo_to_std")    

    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('destination.edit_students'))

    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_student_destinations'))		

    todo = Todo.query.filter(Todo.selected==True).first()
    if todo == None:
        flash("Please select a todo first ")
        return redirect(url_for('students.edit_student_todos'))

    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('students.edit_student_goals'))

    ################################import_pdb;pdb.set_trace()

    statuss = Status.query.all()

    std_todo_is_new = False
    std_todo = Std_todo.query.filter(Std_todo.student_id == std.id).filter(Std_todo.todo_id==todo.id).first()

    if std_todo == None:   #new Std_todo
        std_todo = Std_todo(std.id, todo.id) 
        std_todo_is_new = True

    std_todo.todo_title = todo.title
    std_todo.todo_body = todo.body

    std_todo.todo = todo
    std_todo.student = std    
    std_todo.dst_id = dst.id
    std_todo.goal_id = goal.id

    print("sts ", request.form['selected_status'])
    sts = Status.query.filter(Status.title==request.form['selected_status']).first()
    if sts != None:
        print("selected sts is", sts)   
        std_todo.status_id = sts.id
        std_todo.status_title = sts.title
        std_todo.status_color = sts.color

    who = Accupation.query.filter(Accupation.title==request.form['selected_who']).first() 
    if who != None:    
        print("In match_todo_to_std selected who is", who)   
        std_todo.who_id = who.id
        std_todo.who_title = who.title
           
    std_todo.due_date = request.form['due_date']
    print("In match_todo_to_std selected due_date is", std_todo.due_date)   

    if std_todo_is_new:
        db.session.add(std_todo)
        std.todos.append(std_todo)			
        todo.students.append(std_todo)

    ###############import pdb;;;;; pdb.set_trace()      
    print ("In match_todo_to_std NEW: student date  sts:",  std_todo.todo, std_todo.student, std_todo.due_date, std_todo.status_title, std_todo.due_date)

    std_todo = Std_todo.query.filter(Std_todo.todo_id == todo.id).filter(Std_todo.student_id==std.id).first() 	
    print("New todo is  for std is : Std_todo student is  ", std_todo, std, std_todo.due_date)
    todo.selected = False
    db.session.commit() 
    db.session.refresh(std)
    db.session.refresh(todo)
    db.session.refresh(std_todo)

    ##print("todo_to_student_add METHOD", request.method)
    return  redirect(url_for('students.edit_student_goals')) 
        
        
	
@std.route('/match_todo_to_std2/<int:selected_goal_id>', methods=['GET', 'POST'])
@login_required
def match_todo_to_std2(selected_goal_id):

    goal = goal_select2(selected_goal_id)
    
    print("IN MMMMMMMMM 22222222222 match_todo_to_std2 ", request.form['goal_and_todo_form_button_name'])
    if( int(request.form['goal_and_todo_form_button_name']) % 2 == 0 ):    ### mod 2 is the sign for been goal or todo 
        selected_goal_id = request.form['goal_and_todo_form_button_name']
        selected_goal_id = int(int(selected_goal_id)/2)   
        return match_goal_to_std2(selected_goal_id)
    else:
        selected_todo_id = request.form['goal_and_todo_form_button_name']
        selected_todo_id = int((int(selected_todo_id)-1)/2)
        todo = todo_select2(selected_todo_id)
        g = Goal.query.filter(Goal.selected==True).first()
        print("IN match_todo_to_std2 selected goal todo: ", g, todo)
        return match_todo_to_std()
    
##############END match_todo_to_std ###############	


                                            
@std.route('/try_get_student_todos', methods=['GET', 'POST'])
@login_required
def try_get_student_todos():
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))
        
    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_student_destinations'))		
        

    student_todos = Todo.query.join(Std_todo).filter(Std_todo.dst_id==dst.id).filter(Std_todo.student_id==std.id).all()

    return student_todos


@std.route('/try_get_todos_not_of_student', methods=['GET', 'POST'])
@login_required
def try_get_todos_not_of_student():

    #############################import_pdb; pdb.set_trace()
   
    student = Student.query.filter(Student.selected==True).first()
    if student == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))
    
    std_goal = Std_goal.query.filter(Std_goal.selected==True).first()
    if std_goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('students.edit_student_goals'))		
            
    print(" try_get_todos_not_of_student std  std_goal", student, std_goal)
    #DEBUG
    ###########################impor pdb;pdb.set_trace()	
    ####import_pdb; pdb.set_trace()
    
    all_goal_todos = Todo.query.filter(Todo.goal_id == std_goal.goal_id)
    print("all_goal_todos =: ", all_goal_todos)
    
    student_todos = Todo.query.join(Std_todo).filter(Std_todo.student_id==student.id).filter(Std_todo.todo_id==Todo.id).all()
    print("student_todos =: ", student_todos)

    todos_not_of_student = list(set(all_goal_todos).difference(set(student_todos)))  #todos_not_of_student = all_dst_goal-student_todos
    print("todos_not_of_student =: ", todos_not_of_student)
    
    #############################import_pdb; pdb.set_trace()
    print(" IN try_get_todos_not_of_student todo not of std: ", todos_not_of_student)
    
    return todos_not_of_student



@std.route('/get_dst_todos_not_of_student', methods=['GET', 'POST'])
@login_required
def get_dst_todos_not_of_student():
    
    print(" IN get_todos_not_of_student line 1909 ")
    
    #############################import_pdb; pdb.set_trace()
    ####import_pdb; pdb.set_trace()
    
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))

    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_student_goals'))
                  
    print(" get_todos_not_of_student std  goal", std, dst)

 #DEBUG
    ###########################impor pdb;pdb.set_trace()

    ####import_pdb; pdb.set_trace()

    all_dst_todos = Todo.query.filter(Todo.dst_id == dst.id).all()
    print("all_dst_todos =: ", all_dst_todos)

    student_todos = Todo.query.join(Std_todo).filter(Std_todo.student_id==std.id).filter(Std_todo.dst_id==dst.id).all()
    print("student_todos =: ", student_todos)

    todos_not_of_student = list(set(all_dst_todos).difference(set(student_todos)))  #todos_not_of_student = all_dst_goal-student_todos
    print("todos_not_of_student =: ", todos_not_of_student)

    #############################import_pdb; pdb.set_trace()
    print(" IN get_dst_todos_not_of_student  todos_not_of_student: ", todos_not_of_student)

    return todos_not_of_student




@std.route('/get_goal_todos_not_of_student', methods=['GET', 'POST'])
@login_required
def get_goal_todos_not_of_student():
    
    print(" IN get_todos_not_of_student line 1909 ")
    
    #############################import_pdb; pdb.set_trace()
    ####import_pdb; pdb.set_trace()
    
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))


    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_student_goals'))
                  
    print(" get_todos_not_of_student std  goal", student, goal)

 #DEBUG
    ###########################impor pdb;pdb.set_trace()

    ####import_pdb; pdb.set_trace()

    all_goal_todos = Todo.query.filter(Todo.goal_id == std_goal.goal_id)
    print("all_goal_todos =: ", all_goal_todos)

    student_todos = Todo.query.join(Std_todo).filter(Std_todo.student_id==student.id).filter(Std_todo.goal_id==goal.id).all()
    print("student_todos =: ", student_todos)

    todos_not_of_student = list(set(all_goal_todos).difference(set(student_todos)))  #todos_not_of_student = all_dst_goal-student_todos
    print("todos_not_of_student =: ", todos_not_of_student)

    #############################import_pdb; pdb.set_trace()
    print(" IN try_get_get_goal_todos_not_of_student  todos_not_of_student: ", todos_not_of_student)

    return todos_not_of_student




	
@std.route('/todo_from_student_delete', methods=['GET', 'POST'])
@login_required
def todo_from_std_delete():

    std_todo = Std_todo.query.filter(Std_todo.selected==True).first()
    if std_todo == None:
        flash("Please select a todo first ")
        return redirect(url_for('students.edit_student_todos'))

    db.session.delete(std_todo)
    db.session.commit()

    return  redirect(url_for('students.edit_student_todos'))  #no change in students staff todos
        
@std.route('/todo_from_std_delete2/delete/<int:selected_std_id>/<int:selected_todo_id>', methods=['GET', 'POST'])
@login_required
def todo_from_std_delete2(selected_std_id, selected_todo_id):

    std_todo = std_todo_select2(selected_std_id, selected_todo_id)
    return  redirect(url_for('students.todo_from_std_delete'))  
     
	    
############# END STD TODOS #############################
		

        

############## Student's documents###############	
	
@std.route('/edit_student_documents', methods=['GET', 'POST'])
def edit_student_documents():
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('select.edit_students'))	
        
    ####################################import_pdb; pdb.set_trace()    
    print("In edit_student_documents student std is::: ", std )
    
    return render_template('./documents/edit_std_documents.html', std=std) 
                                                                														  		
@std.route('/edit_student_documents2/<int:selected_student_id>', methods=['GET', 'POST'])
def edit_student_documents2(selected_student_id):
    print("In edit_student_documents2 selected_student_id is :", selected_student_id)
    std = student_select2(selected_student_id)
    return redirect(url_for('students.edit_student_documents'))		

	
@std.route('/document_to_student_add', methods=['GET', 'POST'])
def document_to_student_add():
    author_id = current_user._get_current_object().id

    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('select.edit_students'))	

    if request.method == 'GET':
        return render_template('./documents/document_to_std_add.html', std=std)
    
    print("IN document_to_student_add request is: ", request)
    #get data from form and insert to documentgress db
    title = request.form.get('title')
    body = request.form.get('description')
    
    doc = Document.query.filter(Document.title == title).first()
    if doc != None:
        flash ("document with this name already exist - updating existing document")
        redirect(url_for('students.edit_student_documents'))
    else:
        doc = Document(title, body)

    file_name = request.form.get('file_name')
    uploaded_file = request.files.get('file_name')
    file_name = uploaded_file.filename
    file_data = uploaded_file.read()
    uploaded_file = Ufile(file_name, file_data, author_id)  #find out how to set file_data

    ##############################################import_pdb;pdb.set_trace() 	

    doc.files.append(uploaded_file)

    db.session.add(doc)
    db.session.commit()
    
    ####################################import_pdb; pdb.set_trace()
    
    
    std_doc = Std_document.query.filter(Std_document.document_id==doc.id).filter(Std_document.student_id==std.id).first()
    if std_doc != None:
        flash ("document with this name and this student already exist - updating existing document")
        redirect(url_for('students.edit_student_documents'))  
    else:
        std_doc = Std_document(std.id, doc.id)

    std_doc.title = title
    std_doc.body = body 
    
    std_doc.student=std
    std_doc.document = doc
    
    std.documents.append(std_doc)
    doc.students.append(std_doc)   
        
    db.session.commit()  
    db.session.refresh(doc)
    
    return redirect(url_for('students.edit_student_documents' ))   

@std.route('/document_to_student_add2/<int:selected_student_id>', methods=['GET', 'POST'])
def document_to_student_add2(selected_student_id):
	print("IN document_to_student_add2 std is ::: ", selected_student_id)
	std = student_select2(selected_student_id)
	return redirect(url_for('students.document_to_student_add'))			

	
@std.route('/document_from_student_delete', methods=['GET', 'POST'])
def document_from_student_delete():

    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('select.student_select'))		


    document = Document.query.filter(Document.selected==True).first()
    if document == None:
        flash("Please select a document to delete first ")
        return render_template('edit_student_documents.html', student=student) 
            
    print ("delete selected document is " + document.title + " from slected student " + student.title )

    student.documents.remove(document)
    db.session.commit()  

    return redirect(url_for('students.edit_student_documents')) 

@std.route('/document_from_student_delete2/<int:selected_student_id><int:selected_document_id>', methods=['GET', 'POST'])
#Here author is user_id
def document_from_student_delete2(selected_student_id, selected_document_id):
	std = student_select2(selected_student_id)

	document = document_select2(selected_document_id)
	return redirect(url_for('students.document_from_student_delete')) 	

############## END student's documents###############	