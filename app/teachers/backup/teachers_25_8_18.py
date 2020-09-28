from flask import render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, json
from flask_login import login_user, logout_user, current_user, login_required
#from flask_login import login_manager

from flask_login import LoginManager
from config import basedir
import config

from app import current_app, db
from app.forms import LoginForm
from app import students
from app.templates import *

from app.models import User, Student, Teacher, Profile, Strength, Weaknesse, Role
from app.forms import LoginForm, EditForm

from sqlalchemy import update

from app.content_management import Content


#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
from flask import Blueprint
tchr = Blueprint(
    'teachers', __name__,
    template_folder='templates'
)   
#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
from app import *

@tchr.route('/show_teachers', methods=['POST', 'GET'])
@login_required
def show_teachers():
	print ("in i0ndex show_teachers printing g.user ")
	teachers = Teacher.query.all()
	for teacher in teachers:
		print(teacher.first_name)
	
	return render_template('show_teachers.html',
							teachers=teachers
							)
							
	
@tchr.route('/edit_teacher_students', methods=['GET', 'POST'])
def edit_teacher_students():

	teacher = Teacher.query.filter(Teacher.selected==True).first()
	if teacher == None:
		flash("Please select a teacher first ")
		return redirect(url_for('teachers.teacher_select'))
		
	students = get_teacher_students()	
	print("Students, is empty list: None- Is None- empty list", students, students==None, students is None, students==[])
	for s in students:
		print("IN edit_teacher_students student:", s.id)
	return render_template('edit_teacher_students.html', teacher=teacher, students=students)	

	
@tchr.route('/edit_teacher_students2/edit/<int:selected_teacher_id>/<int:selected_student_id>', methods=['GET', 'POST'])
def edit_teacher_students2(selected_teacher_id, selected_student_id):
	print(selected_teacher_id)
	teacher_select2(selected_teacher_id)
	if selected_student_id != 0:
		print(selected_student_id)
		student_select2(selected_student_id)
	return redirect(url_for('teachers.edit_teacher_students'))
	


@tchr.route('/get_teacher_students', methods=['GET', 'POST'])
def get_teacher_students():
	teacher = Teacher.query.filter(Teacher.selected==True).first()
	if teacher == None:
		flash("Please select a teacher first ")
		return redirect (url_for ('teachers.teacher_select'))
	
	students = Student.query.join(Role).filter(Role.teacher_id==teacher.id).filter(Role.student_id==Student.id).all()
	return students


@tchr.route('/get_students_not_of_teacher', methods=['GET', 'POST'])
def get_students_not_of_teacher():
	teacher = Student.query.filter(Teacher.selected==True).first()
	if student == None:
		flash("Please select a teacher first ")
		return redirect(url_for('teachers.student_select'))
	
	#DEBUG
	#import pdb; pdb.set_trace()	
	all_students = Student.query.all()
	for s in all_students:
		print("TEacher students list :", s.id, s.teachers)
	teacher_students = Student.query.join(Role).filter(Role.teacher_id==Teacher.id).filter(Role.student_id==student.id).all()
	
	for s in teacher_students:
		print("teacher_students:", teacher_students)
	students_with_no_teachers = Student.query.filter(~Student.teachers.any()).all()
	
	students_not_of_teacher = list(set(all_students).difference(set(teacher_students)))  #students_not_of_teacher = all_teachers-teacher_students
	
	teachers_not_in_staff.extend(students_with_no_teachers)
	
	print("student students_not_of_teacher is None   is empt list:", students_not_of_teacher is None, students_not_of_teacher==[])
	for s in students_not_of_teacher:
		print("s from students_not_of_teacher is", s.id)
		for s in t.students:
			print("students NNNNNNNNNOOOOOOOOOOOOOOOTTTTTTTTTTTTTTT IN staff", s.student_id, s.teacher_id, s.title)
	#import pdb; pdb.set_trace()
	#DEBUG

	return students_not_of_teacher



	
#Select a teacher from a list 
@tchr.route('/teacher_select', methods=['GET', 'POST'])
def teacher_select():
	print("1111111111111")
	teachers = Teacher.query.all()
	for teacher in teachers:
		teacher.selected = False
	
	if request.method == 'GET':
		return render_template('teachers.show_teachers.html', teachers=teachers)
		
	print("1111111111111")
		
	selected_teacher_id = int(request.form['selected_teacher'])
	print("1111111111111")

	print ("SSSSSSSSSSSSSelected teacher is" )
	print (selected_teacher_id)

	teacher = Teacher.query.get_or_404(selected_teacher_id)		
		
	teacher.selected = True
	print(teacher.first_name)
	
	db.session.commit()
	
	teacher = Teacher.query.get_or_404(selected_teacher_id)
	print(teacher.selected)
	teachers = Teacher.query.all()
	return render_template('teachers.show_selected_teacher.html', teachers=teachers)

	
#Select a teacher from a list 
@tchr.route('/teacher_select2/<int:selected_teacher_id>', methods=['GET', 'POST'])
def teacher_select2(selected_teacher_id):
	import pdb; pdb.set_trace()
	print("in teacher_select22222222222222222222222222222")
	
	teachers = Teacher.query.all()
	for teacher in teachers:
		teacher.selected = False

	teacher = Teacher.query.get_or_404(selected_teacher_id)		
		
	teacher.selected = True
	print(teacher.first_name)
	
	db.session.commit()
	
	teacher = Teacher.query.get_or_404(selected_teacher_id)
	print(teacher.selected)
	return teacher.id
	'''
	teachers = Teacher.query.all()
	return render_template('show_teachers.html', teachers=teachers)
	'''
	#Select a teacher from a list 
	
			   
#teachers
@tchr.route('/teacher/add/', methods=['GET', 'POST'])
#Here author is user_id
def teacher_add():
	  
	print("RRRRRRRRRRRRRRRRRRRRRRRRRR")
	user = User.query.get_or_404(g.user.id)
	print(g.user)

	#print request
	
	if request.method == 'GET':
		return render_template('add_teacher.html', user=user)
		   
	#get data from form and insert to teacher in teachergress  db
	id = request.form.get('id')
	first_name = request.form.get('first_name')
	last_name = request.form.get('last_name')
	profetional = request.form.get('profetional')
	email = request.form.get('email')
	
	##import pdb; pdb.set_trace() 	
	teacher = Teacher(id, first_name, last_name, profetional, email)	
	
	db.session.add(teacher)	
	db.session.commit()  
	db.session.refresh(teacher)
	# test insert res
	url = url_for('index')
	return redirect(url)   

	
	

@tchr.route('/student_to_teacher_add', methods=['GET', 'POST'])
def student_to_teacher_add():

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
	
	role = Role(student.id, teacher.id, sr)
	
	print("IIIIIIIIIn teacher_to_student_add ", role.student_id, role.teacher_id, role.title)
	role.teacher = teacher
	role.student = student
	
	student.teachers.append(role)			
	teacher.students.append(role) 
		
	print("IIIIIIIIIn updating role ", role.student_id, role.student.id, role.teacher_id,role.teacher.id,  role.title)
   
	db.session.commit() 
	db.session.refresh(student)
	db.session.refresh(teacher)
	
	print("teacher_to_student_add METHOD", request.method)
	return  redirect(url_for('teachers.edit_teacher_students')) 
		
		
	
@tchr.route('/student_to_teacher_add2/add/<int:selected_teacher_id>/<int:selected_student_id>', methods=['GET', 'POST'])
def student_to_teacher_add2(selected_teacher_id, selected_student_id):
	print(selected_student_id)
	student_select2(selected_student_id)
	print(selected_teacher_id)
	teacher_select2(selected_teacher_id)
	return student_to_teacher_add()
	

@tchr.route('/student_to_teacher_add3/add/<int:selected_teacher_id>', methods=['GET', 'POST'])
def student_to_teacher_add3(selected_teacher_id):  #First choose a student to add from students list
	print("1111111111111")
	students = Student.query.filter(Student.hide == False).all()
	for student in students:
		student.selected = False
	
	if request.method == 'GET':
		return render_template('teachers.show_students.html', students=students)
				
	selected_student_id = int(request.form['selected_student'])

	print ("SSSSSSSSSSSSSelected student is" )
	print (selected_student_id)

	student = Student.query.get_or_404(selected_student_id)		
		
	student.selected = True
	print("SSSSSSSSSSSSStudent SSSSSSSSSSSSSelectet", student.first_name)
	
	db.session.commit()
	
	return student_to_teacher_add2(selected_teacher_id, student.id)





		
#update selected teacher
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@tchr.route('/teacher/update/<int:selected_teacher_id>', methods=['GET', 'POST'])
def teacher_update(selected_teacher_id):

	teacher_select2(selected_teacher_id)
		
	teacher = Teacher.query.get_or_404(selected_teacher_id)
	print("In PPPPPPPPPPPPTeacher UUUUUUUUUUUUUUUUUUUUUUpdate")
	print(selected_teacher_id, teacher.id, teacher.first_name)
	
	if request.method == 'GET':
		print("GET render update_teacher.html")
		return render_template('update_teacher.html', teacher=teacher)
		
	#get data from form and insert to teacher in teachergress  db
	#id = request.form.get('id')    #key- can't be changed' unabled for user 
	teacher.first_name = request.form.get('first_name')
	teacher.last_name = request.form.get('last_name')
	teacher.profetional = request.form.get('profetional')
	teacher.email = request.form.get('email')
	
	##import pdb; pdb.set_trace() 		
	db.session.commit()  
	db.session.refresh(teacher)
	# test insert res
	url = url_for('teachers.show_teachers')
	return redirect(url)   
		
@tchr.route('/teacher/delete/', methods=['GET', 'POST'])
#Here author is user_id
def teacher_delete():
	  
	print("RRRRRRRRRRRRRRRRRRRRRRRRRR")
	print(g.user)

	user = User.query.get_or_404(g.user.id)
	author_id = user.id
	
	teacher = Teacher.query.filter(Teacher.selected==True).first()
	if teacher == None:
		flash("Please select a teacher to delete first ")
		return redirect(url_for('teachers.teacher_select'))
			
	print ("delete selected teacher is " )
	print(teacher.first_name)	  

	profiles = Profile.query.join(Teacher.profiles).filter(Teacher.id==teacher.id)
	for profile in profiles:
		profile_delete2(profile.id)		
		
	db.session.delete(teacher) 
	
	db.session.commit()  

	return redirect(url_for('teachers.show_teachers')) 
		
#delete from index teachers list
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@tchr.route('/teacher/delete2/<int:selected_teacher_id>', methods=['GET', 'POST'])
#Here author is user_id
def teacher_delete2(selected_teacher_id):

	print ("SSSSSSSSSSSSSelected teacher is" )
	teacher_select2(selected_teacher_id)
	return teacher_delete()
									   		
