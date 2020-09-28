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
from app.select.select import teacher_select2, student_select2
from app import *

@tchr.route('/show_teachers', methods=['POST', 'GET'])
@login_required

def show_teachers():
	print ("in i0ndex show_teachers printing current_user ")
	teachers = Teacher.query.all()
	for teacher in teachers:
		print(teacher.first_name)
	
	return render_template('show_teachers.html',
							teachers=teachers
							)
							
	
	
##############teacher's students###############	
@tchr.route('/students_by_teacher_show')
@login_required
def students_by_teacher_show():
	#print(" IN students_by_teacher_show")
	teacher = Student.query.filter(Student.selected==True).first()
	if teacher == None:
		flash("Please select a teacher first ")
		return redirect(url_for('select.teacher_select'))
	students = Teacher.query.join(Role).filter(Role.teacher_id==teacher.id).filter(Role.student_id==Teacher.id).all()
	
	students_not_in_staff = Teacher.query.join(Role).filter(Role.teacher_id!=teacher.id).filter(Role.student_id==Teacher.id).all()

		
	teacher_staff_students = Teacher.query.join(Role).filter(Role.teacher_id==teacher.id).filter(Role.student_id==Teacher.id).all()	
	students_not_in_staff = Teacher.query.join(Role).filter(Role.teacher_id!=teacher.id).filter(Role.student_id==Teacher.id).all()

	return render_template('edit_teacher_students.html',
							teacher=teacher,
							teacher_staff_students=teacher_staff_students,
							students_not_in_staff=students_not_in_staff
							)

	
@tchr.route('/students_by_teacher_show2/<int:selected_teacher_id>', methods=['GET', 'POST'])
def students_by_teacher_show2(selected_teacher_id):
	#print(selected_teacher_id)
	student = teacher_select2(selected_teacher_id)
	return redirect(url_for('students_by_teacher_show'))
							

							
@tchr.route('/edit_teacher_students', methods=['GET', 'POST'])
def edit_teacher_students():
	
	teacher = Student.query.filter(Student.selected==True).first()
	if teacher == None:
		flash("Please select a teacher first ")
		return redirect(url_for('select.teacher_select'))
	
	teacher_staff_students = get_teacher_students()
	students_not_in_staff = get_students_not_of_teacher()
	'''
	if request.method == 'POST':
		print(" IN edit_teacher_students method is ", request.method)
		redirect(url_for('teachers.teacher_update', selected_teacher_id=teacher.id))
	'''	
	return render_template('edit_teacher_students.html',    teacher=teacher, 
														   teacher_staff_students=teacher_staff_students,
														   students_not_in_staff=students_not_in_staff)		
	
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
		return redirect(url_for('select.teacher_select'))
	
	#DEBUG
	#import pdb; pdb.set_trace()	
	all_students = Teacher.query.all()
	'''
	for t in all_students:
		#print("TEacher teachers list :", t.id, t.teachers)
	'''
	teacher_staff_students = Teacher.query.join(Role).filter(Role.teacher_id==teacher.id).filter(Role.student_id==Teacher.id).all()

	return teacher_staff_students



@tchr.route('/get_students_not_of_teacher', methods=['GET', 'POST'])
def get_students_not_of_teacher():
	teacher = Teacher.query.filter(Teacher.selected==True).first()
	if teacher == None:
		flash("Please select a teacher first ")
		return redirect(url_for('select.teacher_select'))
	
	#DEBUG
	#import pdb; pdb.set_trace()	
	all_students = Teacher.query.all()
	'''
	for t in all_students:
		#print("TEacher teachers list :", t.id, t.teachers)
	'''
	teacher_staff_students = Student.query.join(Role).filter(Role.teacher_id==teacher.id).filter(Role.student_id==Teacher.id).all()
	
	students_with_no_teachers = Student.query.filter(~Student.teachers.any()).all()
	
	students_not_in_staff = list(set(all_students).difference(set(teacher_staff_students)))  #students_not_in_staff = all_students-teacher_staff_students
	
	students_not_in_staff.extend(students_with_no_teachers)

	#import pdb; pdb.set_trace()
	#DEBUG

	return students_not_in_staff


 
@tchr.route('/student_to_teacher_add', methods=['GET', 'POST'])
def student_to_teacher_add():
	print("IN student_to_teacher_add")
	import pdb; pdb.set_trace()
	teacher = Teacher.query.filter(Teacher.selected==True).first()
	if teacher == None:
		flash("Please select a teacher first ")
		return redirect(url_for('students.teacher_select'))

	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('students.student_select'))
		
	sr = request.form.get('selected_role')
	print("role TTTTTTTTTTTTTtitle:", sr, request.method)


	exist_role = Role.query.filter(Role.teacher_id == teacher.id).filter(Role.student_id==student.id).count()
	
	print("exist_role:", exist_role)
	sr = request.form.get('selected_role')
	print("exist_role:   role title:", exist_role, sr, request.method)
	
	if exist_role == 0:   #new Role
		import pdb; pdb.set_trace()
		role = Role(teacher.id, student.id, sr)
		print("RRRRRRRRRRRRRRRRRRRRRRRrole id", role.teacher_id, role.student_id)
	else:
		role = Role.query.filter(Role.teacher_id == teacher.id).filter(Role.student_id==student.id).first()   #update role
		print("Existing Role is", role)
		print ("Role OLD title for teacher and student :", role.title, role.teacher_id, role.student_id)
		role.title=sr
		print ("Role NEW title :", role.title)

	role.student = student
	role.teacher = teacher
	
	print("IIIIIIIIIIIIIIIIIIIIIIn updating role ",  role.teacher.id, role.student_id, role.title)
	
	teacher.students.append(role)			
	student.teachers.append(role) 
		
	#print("IIIIIIIIIn updating role ", role.teacher_id, role.teacher.id, role.student_id,role.student.id,  role.title)
   
	db.session.commit() 
	db.session.refresh(teacher)
	db.session.refresh(student)
	
	print("student_to_teacher_add METHOD", request.method)
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
		return render_template('show_students.html', students=students)
				
	selected_student_id = int(request.form['selected_student'])

	print ("SSSSSSSSSSSSSelected student is" )
	print (selected_student_id)

	student = Student.query.get_or_404(selected_student_id)		
		
	student.selected = True
	print("SSSSSSSSSSSSStudent SSSSSSSSSSSSSelectet", student.first_name)
	
	db.session.commit()
	
	return student_to_teacher_add2(selected_teacher_id, student.id)
##############teachers students###############	


		
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
	print(current_user)

	user = User.query.get_or_404(current_user.id)
	author_id = user.id
	
	teacher = Teacher.query.filter(Teacher.selected==True).first()
	if teacher == None:
		flash("Please select a teacher to delete first ")
		return redirect(url_for('teachers.teacher_select'))
			
	print ("delete selected teacher is " )
	print(teacher.first_name)	  
	'''
	profiles = Profile.query.join(Teacher.profiles).filter(Teacher.id==teacher.id)
	for profile in profiles:
		profile_delete2(profile.id)		
	'''		
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
									   		
