from flask import render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, json
from flask_login import login_user, logout_user, current_user, login_required
#from flask_login import login_manager

from flask_login import LoginManager
from config import basedir
import config

from app import current_app, db

from app.models import User, Student, Teacher, Profile, Strength, Weaknesse, Role

from app.forms import LoginForm, EditForm
from app import teachers
from app.teachers.teachers import teacher_select2
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
from app.teachers.teachers import teacher_select2
from app import *

@std.route('/')
@std.route('/index', methods=['GET', 'POST'])
@login_required
def index():
	print("CCCCCCCCCCCCCCCCCurent UUUUUUUUUUUUser",  current_user)
	current_user.__repr__()
	'''
	print("current_user sijax is")
	print(current_user.sijax).__repr__()
	'''
	students = Student.query.filter(Student.hide == False).all()
	print("SSSSSSSSSSSSSSSSSSSSSSSStdnts")
	print (students)
	'''	
	return render_template('show_students2.html',
	user=current_user.user,
	students=students
	)
	'''
	return render_template('form6.html')
	
	
@std.route('/show_student_tree', methods=['GET', 'POST'])
def show_student_tree():

	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student to delete first ")
		return redirect(url_for('student_select'))
	print ("ttry selected student is " )

	print(student.first_name)	
	return render_template('lv.html', student=student)

					
@std.route('/show_student_tree2/<int:selected_student_id>', methods=['GET', 'POST'])
def show_student_tree2(selected_student_id):
	print ("SSSSSSSSSSSSSelected student is" )
	student_select2(selected_student_id)
	return show_student_tree()

	
@std.route('/students')
@login_required
def show_students():
	print ("in i0ndex show_students printing current_user.user ")
	students = Student.query.filter(Student.hide==False).all()
	for student in students:
		print(student.first_name)
	
	return render_template('show_students3.html',
							students=students
							)


@std.route('/teachers_by_student_show')
@login_required
def teachers_by_student_show():
	print(" IN teachers_by_student_show")
	student = Student.query.filter(Student.selected==True).first()
	teachers = Teacher.query.join(Role).filter(Role.student_id==student.id).filter(Role.teacher_id==Teacher.id).all()
	
	teachers_not_in_staff = Teacher.query.join(Role).filter(Role.student_id!=student.id).filter(Role.teacher_id==Teacher.id).all()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('student_select'))
		
	student_staff_teachers = Teacher.query.join(Role).filter(Role.student_id==student.id).filter(Role.teacher_id==Teacher.id).all()	
	teachers_not_in_staff = Teacher.query.join(Role).filter(Role.student_id!=student.id).filter(Role.teacher_id==Teacher.id).all()
	for t in student_staff_teachers:
		print("INININININININ teachers_by_student_show teacher:")
		print(t.teacher.first_name, )
	return render_template('edit_student_teachers.html',
							student=student,
							student_staff_teachers=student_staff_teachers,
							teachers_not_in_staff=teachers_not_in_staff
							)

	
@std.route('/teachers_by_student_show2/<int:selected_student_id>', methods=['GET', 'POST'])
def teachers_by_student_show2(selected_student_id):
	print(selected_student_id)
	student_select2(selected_student_id)
	return redirect(url_for('teachers_by_student_show'))
							

@std.route('/edit_student_teachers', methods=['GET', 'POST'])
def edit_student_teachers():
	print("In EEEEEEEEEEEEEEEEE edit_student_teachers")
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('student_select'))
	
	student_staff_teachers = get_student_teachers()
	teachers_not_in_staff = get_teachers_not_of_student()
	'''
	print("teacher teachers_not_in_staff is None   is empt list:", teachers_not_in_staff is None, teachers_not_in_staff==[])
	for t in teachers_not_in_staff:
		print("t from teachers_not_in_staff is", t.id)
		for s in t.students:
			print("teachers NNNNNNNNNOOOOOOOOOOOOOOOTTTTTTTTTTTTTTT IN staff", s, s.student_id, s.teacher_id, s.title)
	'''
	#import pdb; pdb.set_trace()
	#DEBUG
	print("IN edit_student_teachers request method  is ", request)
	if request.method == 'POST':
		redirect(url_for('student_update', selected_student_id=student.id))

	return render_template('edit_student_teachers.html',   student=student, 
														   student_staff_teachers=student_staff_teachers,
														   teachers_not_in_staff=teachers_not_in_staff)		
														  		
@std.route('/edit_student_teachers2/edit/<int:selected_student_id>/<int:selected_teacher_id>', methods=['GET', 'POST'])
def edit_student_teachers2(selected_student_id, selected_teacher_id):
	print(selected_student_id)
	student_select2(selected_student_id)
	if selected_teacher_id != 0:
		print(selected_teacher_id)
		student_select2(selected_teacher_id)
	return edit_student_teachers()
 
 
@std.route('/teacher_to_student_add', methods=['GET', 'POST'])
def teacher_to_student_add():

	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('student_select'))

	teacher = Teacher.query.filter(Teacher.selected==True).first()
	print("In AAAAAAAAAAAA teacher_to_student_add selected teacher is ", teacher.id)
	if teacher == None:
		flash("Please select a teacher first ")
		return redirect(url_for('teacher_select'))
		
	print("SSSSSRRRRR IN teacher_to_student_add")		
	print(student.id)
	print(teacher.id)		
	#Check If This team teacher exist (have Role)  for this student
	exist_role = Role.query.filter(Role.student_id == student.id).filter(Role.teacher_id==teacher.id).count()
	
	print("exist_role:", exist_role)
	sr = request.form.get('selected_role')
	print("exist_role:   role title:", exist_role, sr, request.method)
	
	if exist_role == 0:   #new Role
		role = Role(student.id, teacher.id, sr)
	else:
		role = Role.query.filter(Role.student_id == student.id).filter(Role.teacher_id==teacher.id).first()   #update role
		print("Role is", role)
		print ("Role OLD title for student and teacher :", role.title, role.student_id, role.teacher_id)
		role.title=sr
		print ("Role NEW title for student:", role.title, role.student_id)
		
	print("IIIIIIIIIn teacher_to_student_add ", role.student_id, role.teacher_id, role.title)
	role.teacher = teacher
	role.student = student	
	if exist_role == 0:	#New Role - should be appended to roles list
		student.teachers.append(role)			
		teacher.students.append(role) 
		
	print("IIIIIIIIIn updating role ", role.student_id, role.student.id, role.teacher_id,role.teacher.id,  role.title)
   
	db.session.commit() 
	db.session.refresh(student)
	db.session.refresh(teacher)
	
	print("teacher_to_student_add POST", request.method)
	return  redirect(url_for('students.edit_student_teachers'))  #no change in students staff teachers
		
		
		
@std.route('/teacher_to_student_add2/add/<int:selected_student_id>/<int:selected_teacher_id>', methods=['GET', 'POST'])
def teacher_to_student_add2(selected_student_id, selected_teacher_id):
	role = request.form.get('selected_role')
	print("IIIIIIIIIIIIIIIn teacher_to_student_add2 view student teacher role ", selected_student_id, selected_teacher_id, role)
	
	print(selected_student_id)
	student_select2(selected_student_id)
	import pdb; pdb.set_trace()
	st = redirect(url_for('teachers.teacher_select2', selected_teacher_id=selected_teacher_id))
	st = teachers.teacher_select2(selected_teacher_id)
	print (st.id)
	return teacher_to_student_add()

	
@std.route('/student_from_teacher_delete', methods=['GET', 'POST'])
def student_from_teacher_delete():
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('student_select'))

	teacher = Teacher.query.filter(Teacher.selected==True).first()
	if teacher == None:
		flash("Please select a teacher first ")
		return redirect(url_for('teacher_select'))
		
	print("SSSSSRRRRR IN teacher_to_student_add")		
	print(student.id)
	print(teacher.id)		

	role = Role.query.filter(Role.student_id == student.id).filter(Role.teacher_id==teacher.id).first()   #update role
	print("Role is", role)
	print ("Role OLD title for student and teacher :", role.title, role.student_id, role.teacher_id)
	role.title=sr
	print ("Role NEW title for student:", role.title, role.student_id)
	
	print("IIIIIIIIIn teacher_to_student_add ", role.student_id, role.teacher_id, role.title)
	role.teacher = teacher
	role.student = student	
	if exist_role == 0:	#New Role - should be appended to roles list
		student.teachers.remove(role)			
		teacher.students.remove(role) 
		
	print("IIIIIIIIIn updating role ", role.student_id, role.student.id, role.teacher_id,role.teacher.id,  role.title)
   
	db.session.commit() 
	db.session.refresh(student)
	db.session.refresh(teacher)
	
	print("teacher_to_student_add POST", request.method)
	return  redirect(url_for('edit_student_teachers'))  #no change in students staff teachers
		
@std.route('/student_from_teacher_delete2/add/<int:selected_teacher_id>/<int:selected_student_id>', methods=['GET', 'POST'])
def student_from_teacher_delete2(selected_teacher_id, selected_student_id):
	print(selected_student_id)
	student_select2(selected_student_id)
	if selected_teacher_id:
		print(selected_teacher_id)
		student_select2(selected_teacher_id)
	return teacher_to_student_delete()

	
	
	
@std.route('/get_student_teachers', methods=['GET', 'POST'])
def get_student_teachers():
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('student_select'))
	
	#DEBUG
	#import pdb; pdb.set_trace()	
	all_teachers = Teacher.query.all()
	'''
	for t in all_teachers:
		print("TEacher students list :", t.id, t.students)
	'''
	student_staff_teachers = Teacher.query.join(Role).filter(Role.student_id==student.id).filter(Role.teacher_id==Teacher.id).all()

	return student_staff_teachers




@std.route('/get_teachers_not_of_student', methods=['GET', 'POST'])
def get_teachers_not_of_student():
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('student_select'))
	
	#DEBUG
	#import pdb; pdb.set_trace()	
	all_teachers = Teacher.query.all()
	'''
	for t in all_teachers:
		print("TEacher students list :", t.id, t.students)
	'''
	student_staff_teachers = Teacher.query.join(Role).filter(Role.student_id==student.id).filter(Role.teacher_id==Teacher.id).all()
	
	for t in student_staff_teachers:
		print("student_staff_teachers:", student_staff_teachers)
	teachers_with_no_students = Teacher.query.filter(~Teacher.students.any()).all()
	
	teachers_not_in_staff = list(set(all_teachers).difference(set(student_staff_teachers)))  #teachers_not_in_staff = all_teachers-student_staff_teachers
	
	teachers_not_in_staff.extend(teachers_with_no_students)
	'''
	print("teacher teachers_not_in_staff is None   is empt list:", teachers_not_in_staff is None, teachers_not_in_staff==[])
	for t in teachers_not_in_staff:
		print("t from teachers_not_in_staff is", t.id)
		for s in t.students:
			print("teachers NNNNNNNNNOOOOOOOOOOOOOOOTTTTTTTTTTTTTTT IN staff", s, s.student_id, s.teacher_id, s.title)
	'''
	#import pdb; pdb.set_trace()
	#DEBUG

	return teachers_not_in_staff





														   
#Select a student from a list 
@std.route('/student_select', methods=['GET', 'POST'])
def student_select():
	print("1111111111111")
	students = Student.query.filter(Student.hide == False).all()
	for student in students:
		student.selected = False
	
	if request.method == 'GET':
		return render_template('show_students.html', students=students)
		
	print("1111111111111")
		
	selected_student_id = int(request.form['selected_student'])
	print("1111111111111")

	print ("SSSSSSSSSSSSSelected student is" )
	print (selected_student_id)

	student = Student.query.get_or_404(selected_student_id)		
		
	student.selected = True
	print(student.first_name)
	
	db.session.commit()
	
	student = Student.query.get_or_404(selected_student_id)
	print(student.selected)
	students = Student.query.filter(Student.hide == False).all()
	#return render_template('show_selected_student.html', students=students)
	return show_students()

	
#Select a student from a list 
@std.route('/student_select2/<int:selected_student_id>', methods=['GET', 'POST'])
def student_select2(selected_student_id):
	print("in student_select22222222222222222222222222222")
	
	students = Student.query.filter(Student.hide == False).all()
	for student in students:
		student.selected = False

	student = Student.query.get_or_404(selected_student_id)		
		
	student.selected = True
	print(student.first_name)
	
	db.session.commit()
	
	student = Student.query.get_or_404(selected_student_id)
	print(student.selected)
	students = Student.query.filter(Student.hide == False).all()
	return render_template('show_selected_student.html', students=students)
	
	#Select a student from a list 
	
			   
@std.route('/student/add/', methods=['GET', 'POST'])
#Here author is user_id
def student_add():
	  
	print("RRRRRRRRRRRRRRRRRRRRRRRRRR")
	user = User.query.get_or_404(current_user.id)
	print(current_user.id)

	#print request
	
	if request.method == 'GET':
		return render_template('add_student.html', user=user)
		   
	#get data from form and insert to student in studentgress  db
	id = request.form.get('id')
	first_name = request.form.get('first_name')
	last_name = request.form.get('last_name')
	birth_date = request.form.get('birth_date')
	grade = request.form.get('grade')
	
	student_already_exist = Student.query.filter(Student.id == id).first()
	print(student_already_exist)
	if student_already_exist is not []:  #Student already exist in system probably in hide mode
		flash("This student already exists in system", student_already_exist.id)
		return render_template('un_hide_student.html', student_already_exist=student_already_exist)

	###import pdb; pdb.set_trace() 	Enter new student to DB
	student = Student(id, first_name, last_name, birth_date, grade)	
	
	db.session.add(student)	
	db.session.commit()  
	db.session.refresh(student)
	# test insert res
	url = url_for('show_students')
	return redirect(url)   


@std.route('/student/unhide/<int:selected_student_id>', methods=['GET', 'POST'])
#Here author is user_id
def student_unhide2(selected_student_id):
	  
	print("In UUUUUUUUUUUnhide2 student    method", selected_student_id, request.method)
	user = User.query.get_or_404(current_user.id)
	print(current_user.id)

	#print request		
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

	student_select2(selected_student_id)
		
	student = Student.query.get_or_404(selected_student_id)
	print("In PPPPPPPPPPPPStudent UUUUUUUUUUUUUUUUUUUUUUpdate")
	print(selected_student_id, student.id, student.first_name)
	
	if request.method == 'GET':
		print("GET render update_student.html")
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
	url = url_for('show_students')
	return redirect(url)   	
	return redirect(url_for('index'))
	
		
@std.route('/student/delete/', methods=['GET', 'POST'])
#Here author is user_id
def student_delete():
	  
	print("RRRRRRRRRRRRRRRRRRRRRRRRRR")
	print(current_user.user)

	user = User.query.get_or_404(current_user.user.id)
	author_id = user.id
	
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student to delete first ")
		return redirect(url_for('student_select'))
			
	print ("delete selected student is " )
	print(student.first_name)
	student.hide = True
	'''
	profile = Profile.query.join(Student.profile).filter(Student.id==student.id)
	profile_delete()
	db.session.delete(student) 
	'''
	db.session.commit()  

	return redirect(url_for('index')) 
		
#delete from index students list
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@std.route('/student/delete2/<int:selected_student_id>', methods=['GET', 'POST'])
#Here author is user_id
def student_delete2(selected_student_id):

	print ("SSSSSSSSSSSSSelected student is" )
	student_select2(selected_student_id)
	return student_delete()












	
