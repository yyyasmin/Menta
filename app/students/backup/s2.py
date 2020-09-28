from flask import render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, json
from flask_login import login_user, logout_user, current_user, login_required
#from flask_login import login_manager

from flask_login import LoginManager
from config import basedir
import config

from app import  db
from app.models import User, Student, Teacher, Profile, Strength, Weaknesse, Role

from app.forms import LoginForm, EditForm
from app.select.select import teacher_select2, student_select2, profile_select2

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
from app.models import User, School, Student, Profile, Strength, Weaknesse, Role

################
#### config ####
################

std = Blueprint(
    'students', __name__,
    template_folder='templates'
) 
from app.select.select import teacher_select2, student_select2
from app import *

@std.route('/')
@std.route('/index', methods=['GET', 'POST'])
@login_required
def index():
	#print("CCCCCCCCCCCCCCCCCurent UUUUUUUUUUUUser",  current_user)
	current_user.__repr__()
	'''
	#print("current_user sijax is")
	#print(current_user.sijax).__repr__()
	'''
	#Reset student selection
	students = Student.query.all()
	for std in students:
		#print("IN INDExxxxxxxxxxxxxxxxxxxxx UUU nselectingstd: ", std.id)
		std.selected = False
	db.session.commit() 
	#Reset student selection

	students = Student.query.filter(Student.hide == False).all()
	#print("SSSSSSSSSSSSSSSSSSSSSSSStdnts")
	#print (students)

	return render_template('form6.html')


@std.route('/student_home' )
def student_home():
	print("in student_home")
	return render_template('form6.html')
	
		
@std.route('/show_student_tree', methods=['GET', 'POST'])
def show_student_tree():

	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student to delete first ")
		return redirect(url_for('select.student_select'))

	print("selected student for tree show is " + str(student.id))	
	print("printing students tree")
	for dest in student.destinations:
		print("dest title: ", dest.title)
		for goal in dest.goals:
			print("dest - goal title", dest.title, goal.title)
	return render_template('show_students_tree.html', student=student)

					
@std.route('/show_student_tree2/<int:selected_student_id>', methods=['GET', 'POST'])
def show_student_tree2(selected_student_id):
	#print ("SSSSSSSSSSSSSelected student is" )
	std = student_select2(selected_student_id)
	return redirect(url_for('students.show_student_tree'))

	
@std.route('/students')
@login_required
def show_students():
	#print ("in i0ndex show_students #printing current_user.user ")
	students = Student.query.filter(Student.hide==False).all()
		
	return render_template('show_students3.html',
							students=students
							)
							
							
@std.route('/get_dummy_student', methods=['GET', 'POST'])
def get_dummy_student():

	dummy_std = Student.query.filter(Student.first_name=='Dummy').first()
	print(dummy_std)
	#import pdb; pdb.set_trace()
	if dummy_std:
		return dummy_std
	else:
		print("dummy_std does not exist creating new one dummy_std is: ", dummy_std)
		dummy_std = Student(0, 'Humpty', 'Dumpty', datetime.utcnow(), 'D')
		dummy_std.hide=True
		db.session.add(dummy_std)	
		db.session.commit()  
		db.session.refresh(dummy_std)
		print("Created dummy std id first_name: ", dummy_std.id, dummy_std.first_name)
	return dummy_std
								
@std.route('/student/add/', methods=['GET', 'POST'])
def student_add():
	  
	#print("RRRRRRRRRRRRRRRRRRRRRRRRRR")
	user = User.query.get_or_404( current_user._get_current_object().id)
	#print(current_user._get_current_object().id)

	##print request
	
	if request.method == 'GET':
		return render_template('add_student.html', user=user)
		   
	#get data from form and insert to student in studentgress  db
	id = request.form.get('id')
	first_name = request.form.get('first_name')
	last_name = request.form.get('last_name')
	birth_date = request.form.get('birth_date')
	grade = request.form.get('grade')
	
	student_already_exist = Student.query.filter(Student.id == id).first()
	#import pdb; pdb.set_trace()
	print(student_already_exist)
	if student_already_exist is not None :  #Student already exist in system probably in hide mode
		flash("This student already exists in system", student_already_exist.id)
		return render_template('un_hide_student.html', student_already_exist=student_already_exist)

	###import pdb; pdb.set_trace() 	Enter new student to DB
	student = Student(id, first_name, last_name, birth_date, grade)	
	
	new_profile = Profile('New profile', 'No description yet')
	db.session.add(new_profile)	
	db.session.commit() 	
	db.session.refresh(new_profile)
	#import pdb; pdb.set_trace()
	print(new_profile.id)
	student.profile_id = new_profile.id
	
	db.session.add(student)	
	db.session.commit()  
	db.session.refresh(student)
	
	url = url_for('students.show_students')
	return redirect(url)   


@std.route('/student/unhide/<int:selected_student_id>', methods=['GET', 'POST'])
#Here author is user_id
def student_unhide2(selected_student_id):
	  
	#print("In UUUUUUUUUUUnhide2 student    method", selected_student_id, request.method)
	user = User.query.get_or_404(current_user._get_current_object().id)
	print(current_user._get_current_object().id)

	##print request		
	student = Student.query.filter(Student.id==selected_student_id).first()
	student.hide = False
	db.session.commit()  
	db.session.refresh(student)
	url = url_for('students.show_students')
	return redirect(url)


	
#update selected student
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@std.route('/student/update/<int:selected_student_id>', methods=['GET', 'POST'])
def student_update(selected_student_id):

	std = student_select2(selected_student_id)
		
	student = Student.query.get_or_404(selected_student_id)
	#print("In PPPPPPPPPPPPStudent UUUUUUUUUUUUUUUUUUUUUUpdate")
	#print(selected_student_id, student.id, student.first_name)
	
	if request.method == 'GET':
		#print("GET render update_student.html")
		return render_template('update_student.html', student=student)
  
	#get data from form and insert to student in studentgress  db
	#student.id = request.form.get('id')    #not updateable the field apears disabled for user 
	student.first_name = request.form.get('first_name')
	student.last_name = request.form.get('last_name')
	student.birth_date = request.form.get('birth_date')
	student.grade = request.form.get('grade')
	
	#db.session.update(student)	
	db.session.commit()  
	db.session.refresh(student)
	# test insert res
	url = url_for('students.show_students')
	return redirect(url)   	
	return redirect(url_for('index'))
	
		
@std.route('/student/delete/', methods=['GET', 'POST'])
#Here author is user_id
def student_delete():
	  
	#print("RRRRRRRRRRRRRRRRRRRRRRRRRR")
	print(current_user._get_current_object().id)

	user = User.query.get_or_404(current_user._get_current_object().id)
	author_id = user.id
	
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student to delete first ")
		return redirect(url_for('select.student_select'))
			
	student.hide = True
	db.session.commit()  

	return redirect(url_for('students.index')) 
		
#delete from index students list
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@std.route('/student/delete2/<int:selected_student_id>', methods=['GET', 'POST'])
#Here author is user_id
def student_delete2(selected_student_id):

	#print ("SSSSSSSSSSSSSelected student is", selected_student_id )
	std = student_select2(selected_student_id)
	#print(" IN student_delete2 dddddddddeleting student :", std.id)
	return student_delete()

	
	
##############studets teachers###############	
@std.route('/teachers_by_student_show')
@login_required
def teachers_by_student_show():
	#print(" IN teachers_by_student_show")
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('select.student_select'))
	teachers = Teacher.query.join(Role).filter(Role.student_id==student.id).filter(Role.teacher_id==Teacher.id).all()
	
	teachers_not_in_staff = Teacher.query.join(Role).filter(Role.student_id!=student.id).filter(Role.teacher_id==Teacher.id).all()

		
	student_staff_teachers = Teacher.query.join(Role).filter(Teacher.hide==False).filter(Role.student_id==student.id).filter(Role.teacher_id==Teacher.id).all()	
	teachers_not_in_staff = Teacher.query.join(Role).filter(Teacher.hide==False).filter(Role.student_id!=student.id).filter(Role.teacher_id==Teacher.id).all()

	return render_template('edit_student_teachers.html',
							student=student,
							student_staff_teachers=student_staff_teachers,
							teachers_not_in_staff=teachers_not_in_staff
							)

	
@std.route('/teachers_by_student_show2/<int:selected_student_id>', methods=['GET', 'POST'])
def teachers_by_student_show2(selected_student_id):
	#print(selected_student_id)
	std = student_select2(selected_student_id)
	return redirect(url_for('teachers_by_student_show'))
							

@std.route('/edit_student_teachers', methods=['GET', 'POST'])
def edit_student_teachers():
	
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('select.student_select'))
	
	student_staff_teachers = get_student_teachers()
	teachers_not_in_staff = get_teachers_not_of_student()

	return render_template('edit_student_teachers.html',   student=student, 
														   student_staff_teachers=student_staff_teachers,
														   teachers_not_in_staff=teachers_not_in_staff)		
														  		
@std.route('/edit_student_teachers2/edit/<int:selected_student_id>/<int:selected_teacher_id>', methods=['GET', 'POST'])
def edit_student_teachers2(selected_student_id, selected_teacher_id):
	print("In edit_student_teachers2 Request is :", request)
	std = student_select2(selected_student_id)
	if selected_teacher_id != 0:
		tchr = teacher_select2(selected_teacher_id)
	return edit_student_teachers()
 
 
@std.route('/teacher_to_student_add', methods=['GET', 'POST'])
def teacher_to_student_add():
	print("IN teacher_to_student_add")
	#import pdb; pdb.set_trace()
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('teachers.student_select'))

	teacher = Teacher.query.filter(Teacher.selected==True).first()
	if teacher == None:
		flash("Please select a teacher first ")
		return redirect(url_for('teachers.teacher_select'))
		
	sr = request.form.get('selected_role')
	print("role TTTTTTTTTTTTTtitle:", sr, request.method)


	exist_role = Role.query.filter(Role.student_id == student.id).filter(Role.teacher_id==teacher.id).count()
	
	print("exist_role:", exist_role)
	sr = request.form.get('selected_role')
	print("exist_role:   role title:", exist_role, sr, request.method)
	
	if exist_role == 0:   #new Role
		#import pdb; pdb.set_trace()
		role = Role(student.id, teacher.id, sr)
		print("RRRRRRRRRRRRRRRRRRRRRRRrole id", role.student_id, role.teacher_id)
	else:
		role = Role.query.filter(Role.student_id == student.id).filter(Role.teacher_id==teacher.id).first()   #update role
		print("Existing Role is", role)
		print ("Role OLD title for student and teacher :", role.title, role.student_id, role.teacher_id)
		role.title=sr
		print ("Role NEW title :", role.title)

	role.teacher = teacher
	role.student = student
	
	print("IIIIIIIIIIIIIIIIIIIIIIn updating role ",  role.student.id, role.teacher_id, role.title)
	
	student.teachers.append(role)			
	teacher.students.append(role)
	#DEBUG
	role = Role.query.filter(Role.teacher_id == teacher.id).filter(Role.student_id==student.id).first() 	
	print("New eole title is: ", role.title)
	#DEBUG
	db.session.commit() 
	db.session.refresh(student)
	db.session.refresh(teacher)
	
	print("teacher_to_student_add METHOD", request.method)
	return  redirect(url_for('students.edit_student_teachers')) 
		
		
	
@std.route('/teacher_to_student_add2/add/<int:selected_teacher_id>/<int:selected_student_id>', methods=['GET', 'POST'])
def teacher_to_student_add2(selected_teacher_id, selected_student_id):
	print(selected_student_id)
	student_select2(selected_student_id)
	print(selected_teacher_id)
	teacher_select2(selected_teacher_id)
	return teacher_to_student_add()
	

	
@std.route('/student_from_teacher_delete', methods=['GET', 'POST'])
def student_from_teacher_delete():
	#import pdb; pdb.set_trace()
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('select.student_select'))

	teacher = Teacher.query.filter(Teacher.selected==True).first()
	if teacher == None:
		flash("Please select a teacher first ")
		return redirect(url_for('select.teacher_select'))
		
	#print("SSSSSRRRRR IN student_from_teacher_delete   deleteing student %s from teacher %s :",student.id, teacher.id )			

	role = Role.query.filter(Role.student_id == student.id).filter(Role.teacher_id==teacher.id).first()   #update role
	if role:
		print ("DEleting OLD ROLE ", role.title)
		role.title = "No Role"

   
	db.session.commit() 
	db.session.refresh(student)
	db.session.refresh(teacher)
	
	#DEBUG
	if role:
		role = Role.query.filter(Role.student_id == student.id).filter(Role.teacher_id==teacher.id).first()   #update role
		print ("NEW ROLE IS ", role.title)
	#DEBUG
	
	return  redirect(url_for('students.edit_student_teachers'))  #no change in students staff teachers
		
@std.route('/student_from_teacher_delete2/delete/<int:selected_teacher_id>/<int:selected_student_id>', methods=['GET', 'POST'])
def student_from_teacher_delete2(selected_teacher_id, selected_student_id):
	#print("In DDDDDDDDDDDD student_from_teacher_delete2")
	std = student_select2(selected_student_id)
	if selected_teacher_id:
		#print(selected_teacher_id)
		tchr = teacher_select2(selected_teacher_id)
	return  redirect(url_for('students.student_from_teacher_delete'))  

	
	
@std.route('/get_student_teachers', methods=['GET', 'POST'])
def get_student_teachers():
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('select.student_select'))
	
	#DEBUG
	#import pdb; pdb.set_trace()	
	all_teachers = Teacher.query.all()
	'''
	for t in all_teachers:
		#print("TEacher students list :", t.id, t.students)
	'''
	student_staff_teachers = Teacher.query.join(Role).filter(Teacher.hide==False).filter(Role.student_id==student.id).filter(Role.teacher_id==Teacher.id).all()

	return student_staff_teachers



@std.route('/get_teachers_not_of_student', methods=['GET', 'POST'])
def get_teachers_not_of_student():
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('select.student_select'))
	
	#DEBUG
	#import pdb; pdb.set_trace()	
	all_teachers = Teacher.query.filter(Teacher.hide==False).all()
	'''
	for t in all_teachers:
		#print("TEacher students list :", t.id, t.students)
	'''
	student_staff_teachers = Teacher.query.join(Role).filter(Teacher.hide==False).filter(Role.student_id==student.id).filter(Role.teacher_id==Teacher.id).all()
	
	teachers_with_no_students = Teacher.query.filter(Teacher.hide==False).filter(~Teacher.students.any()).all()
	
	teachers_not_in_staff = list(set(all_teachers).difference(set(student_staff_teachers)))  #teachers_not_in_staff = all_teachers-student_staff_teachers
	
	teachers_not_in_staff.extend(teachers_with_no_students)

	#import pdb; pdb.set_trace()
	#DEBUG

	return teachers_not_in_staff
##############studets teachers###############	


	
##############studets profiles###############	
@std.route('/profile_by_student_show')
@login_required
def profile_by_student_show():

	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('students.index'))


	#import pdb; pdb.set_trace()
	return render_template('edit_students_profile.html',
							student=student,
							)

	
@std.route('/profile_by_student_show2/<int:selected_student_id>', methods=['GET', 'POST'])
def profile_by_student_show2(selected_student_id):
	#print(selected_student_id)
	std = student_select2(selected_student_id)
	return redirect(url_for('student.profile_by_student_show'))
							

@std.route('/edit_students_profile', methods=['GET', 'POST'])
def edit_students_profile():
	#import pdb; pdb.set_trace()
	print("in edit_students_profile")
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('select.student_select'))

	profile = Profile.query.filter(student.profile_id == Profile.id).first()
	'''
	if profile:
		return render_template('edit_students_profile.html', student=student,
															 profile=profile)
	else:
		return redirect(url_for('student.profile_to_student_add2', selected_student_id=student.id))
	'''
	#import pdb; pdb.set_trace()
	print("In edit_students_profile calling edit_students_profile html ", student.id, profile.id)
	return render_template('edit_students_profile.html', student=student,
														 profile=profile)
	
														  		
@std.route('/edit_students_profile2/edit/<int:selected_student_id>/<int:selected_profile_id>', methods=['GET', 'POST'])
def edit_students_profile2(selected_student_id, selected_profile_id):
	print("In edit_students_profile2 Request is :", request)
	std = student_select2(selected_student_id)
	profile = Profile.query.filter(std.profile_id == Profile.id).first()
	'''
	if profile:
		prf = profile_select2(selected_profile_id)
	else:
		return profile_to_student_add()
	'''
	return edit_students_profile()
 
 
@std.route('/profile_to_student_add', methods=['GET', 'POST'])
def profile_to_student_add():
	print("In profile_to_student_add")
	user = User.query.get_or_404(current_user._get_current_object().id)
	author_id = user.id
		
	student = Student.query.filter(Student.selected==True).first()

	if student == None:
		flash("Please select an student first ")
		return redirect(url_for('select.student_select'))
	#print request

	if request.method == 'GET':
		return render_template('profile_to_student_add.html', student=student)
		   
	#get data from form and insert to postgress db
	title = request.form.get('title')
	body = request.form.get('body')

	#import pdb; pdb.set_trace() 	
	profile = Profile(title, body, author_id)	

	student.profile = profile
	   
	db.session.add(profile) 	
	db.session.commit()  
	db.session.refresh(profile)
	
	print("In profile_to_student_add", student.id, profile.id)

	url = url_for('students.edit_students_profile2', selected_student_id=student.id, selected_profile_id=profile.id )
	return redirect(url)   
	
@std.route('/profile_to_student_add2/add/<int:selected_student_id>', methods=['GET', 'POST'])
def profile_to_student_add2(selected_student_id):
	#print("In DDDDDDDDDDDD profile_from_student_delete2")
	std = student_select2(selected_student_id)
	return  redirect(url_for('students.profile_to_student_add'))  

	
@std.route('/profile_from_student_delete', methods=['GET', 'POST'])
def profile_from_student_delete():
	#import pdb; pdb.set_trace()
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('select.student_select'))

	profile = Profile.query.filter(Profile.selected==True).first()
	if profile == None:
		flash("Please select a profile first ")
		return redirect(url_for('select.profile_select'))
	
	#print("SSSSSRRRRR IN profile_from_student_delete   deleteing student %s from profile %s :",student.id, profile.id )			

	print("deleteint profile from student %s ", profile.title)		
	db.session.delete(profile)		
	db.session.commit() 
	
	return  redirect(url_for('students.edit_students_profile'))  #no change in students staff profiles
		
@std.route('/profile_from_student_delete2/delete/<int:selected_student_id>/<int:selected_profile_id>', methods=['GET', 'POST'])
def profile_from_student_delete2(selected_student_id, selected_profile_id):
	#print("In DDDDDDDDDDDD profile_from_student_delete2")
	std = student_select2(selected_student_id)
	if selected_profile_id:
		#print(selected_profile_id)
		prf = profile_select2(selected_profile_id)
	return  redirect(url_for('students.profile_from_student_delete'))  

	
	
@std.route('/get_students_profile', methods=['GET', 'POST'])
def get_students_profile():
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('select.student_select'))

	profile = Profile.query.join(Student.pros).filter(Student.id==student.id)	
	return profile

##############studets profiles###############	


##############studets destinations###############	
@std.route('/destinations_by_student_show')
@login_required
def destinations_by_student_show():

	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('students.destinations_by_student_show'))

	#import pdb; pdb.set_trace()
	return render_template('edit_students_destinations.html', student=student)

		
@std.route('/destinations_by_student_show2/<int:selected_student_id>', methods=['GET', 'POST'])
def destinations_by_student_show2(selected_student_id):
	#print(selected_student_id)
	std = student_select2(selected_student_id)
	return redirect(url_for('destinations_by_student_show'))
							

@std.route('/edit_students_destinations', methods=['GET', 'POST'])
def edit_students_destinations():
	
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('select.student_select'))		

	return render_template('edit_students_destinations.html', student=student) 
																
														  		
@std.route('/edit_students_destinations2/edit/<int:selected_student_id>/<int:selected_destination_id>', methods=['GET', 'POST'])
def edit_students_destinations2(selected_student_id, selected_destination_id):
	print("In edit_student_destinations2 Request is :", request)
	std = student_select2(selected_student_id)
	if selected_destination_id != 0:
		dest = destination_select2(selected_destination_id)
	return redirect(url_for('students.edit_students_destinations'))		

	
@std.route('/destination_to_student_add', methods=['GET', 'POST'])
def destination_to_student_add():
	
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('select.student_select'))		

	if request.method == 'GET':
		return render_template('add_destination_to_student.html', student=student)
		   
	#get data from form and insert to destinationgress db
	title = request.form.get('title')
	body = request.form.get('description')
	tag_title = request.form.get('tag')

	#import pdb; pdb.set_trace() 	
	author_id = current_user._get_current_object().id
	destination = Destination(title, body, author_id)	

	tag = Tag.query.filter(Tag.title==tag_title).first()	
	if tag == None:	    	     
		tag = Tag(tag_title)	
		print(tag.title)				
		db.session.add(tag)
		
	destination.tags.append(tag)	
	student.destinations.append(destination)   
	   
	db.session.add(destination)    
	db.session.commit()  
	db.session.refresh(destination)
	# test insert res
	url = url_for('students.destinations_by_student_show')
	return redirect(url)   

@std.route('/destination_to_student_add2/<int:selected_student_id>', methods=['GET', 'POST'])
def destination_to_student_add2(selected_student_id):
	print(selected_student_id)
	std = student_select2(selected_student_id)
	return redirect(url_for('students.destination_to_student_add'))			

	
@std.route('/destination_from_student_delete', methods=['GET', 'POST'])
def destination_from_student_delete():
	
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('select.student_select'))		


	destination = Destination.query.filter(Destination.selected==True).first()
	if destination == None:
		flash("Please select a destination to delete first ")
		return redirect(url_for('select.destination_select'))
			
	print ("delete selected destination is " )
	print(destination.title)      
	
	student.destinations.remove(destination)
	db.session.commit()  

	return redirect(url_for('students.index')) 

@std.route('/destination_from_student_delete2/<int:selected_student_id><int:selected_destination_id>', methods=['GET', 'POST'])
#Here author is user_id
def destination_from_student_delete2(selected_student_id, selected_destination_id):

	std = destination_select2(selected_student_id)
	dest = destination_select2(selected_destination_id)
	return redirect(url_for('students.student_from_destination_delete')) 	

##############studets destinations###############	















	
