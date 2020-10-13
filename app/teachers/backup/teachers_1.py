from flask import render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, json
from flask_login import login_user, logout_user, current_user, login_required
#from flask_login import login_manager

from flask_login import LoginManager
from config import basedir
import config

from app import  db
from app.models import User, Teacher, Student, Profile, Strength, Weakness, Role

from app.forms import LoginForm, EditForm
from app.select.select import student_select2, teacher_select2, profile_select2

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
from app.models import User, School, Teacher, Profile, Strength, Weakness, Role

################
#### config ####
################

tchr = Blueprint(
    'teachers', __name__,
    template_folder='templates'
) 
from app.select.select import student_select2, teacher_select2
from app import *


@tchr.route('/teacher_home' )
@login_required
def teacher_home():
	print("in teacher_home")
	return render_template('form6.html')
			
	
@tchr.route('/edit_teacher_tree', methods=['GET', 'POST'])
@login_required
def edit_teacher_tree():

	teacher = Teacher.query.filter(Teacher.selected==True).first()
	if teacher == None:
		flash("Please select a teacher to delete first ")
		return redirect(url_for('select.teacher_select'))
	#print ("ttry selected teacher is " )

	#print(teacher.first_name)	
	return render_template('lv.html', teacher=teacher)

					
@tchr.route('/edit_teacher_tree2/<int:selected_teacher_id>', methods=['GET', 'POST'])
def edit_teacher_tree2(selected_teacher_id):
	#print ("SSSSSSSSSSSSSelected teacher is" )
	student = teacher_select2(selected_teacher_id)
	return edit_teacher_tree()

	
@tchr.route('/teachers')
@login_required
def edit_teachers():
	print ("in i0ndex edit_teachers #printing current_user.user ")
	teachers = Teacher.query.filter(Teacher.hide==False).all()
	return render_template('edit_teachers.html',
							teachers=teachers
							)

								
@tchr.route('/teacher/add/', methods=['GET', 'POST'])
@login_required
def teacher_add():

    author_id = current_user._get_current_object().id
      
    if request.method == 'GET':
        return render_template('add_teacher.html', user=author_id)
           
    id = request.form.get('id')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    birth_date = request.form.get('birth_date')

    profetional = request.form.get('profetional')
    email = request.form.get('email')

    teacher_already_exist = Teacher.query.filter(Teacher.id == id).first()
    print(teacher_already_exist)
    if teacher_already_exist is not None :  #Teacher already exist in system probably in hide mode
        flash("This teacher already exists in system", teacher_already_exist.id)
        return render_template('un_hide_teacher.html', teacher_already_exist=teacher_already_exist)

    ####import pdb; pdb.set_trace() 	Enter new teacher to DB
    teacher = Teacher(id, first_name, last_name, birth_date, profetional, email, author_id)

    db.session.add(teacher)	
    db.session.commit()  
    db.session.refresh(teacher)
    # test insert res
    url = url_for('teachers.edit_teachers')
    return redirect(url)   


@tchr.route('/teacher/unhide/<int:selected_teacher_id>', methods=['GET', 'POST'])
@login_required
def teacher_unhide2(selected_teacher_id):
	  
	#print("In UUUUUUUUUUUnhide2 teacher    method", selected_teacher_id, request.method)
	user = User.query.get_or_404(current_user.id)
	#print(current_user.id)

	##print request		
	teacher = Teacher.query.filter(Teacher.id==selected_teacher_id).first()
	teacher.hide = False
	db.session.commit()  
	db.session.refresh(teacher)
	url = url_for('teachers.edit_teachers')
	return redirect(url)


	
#update selected teacher
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@tchr.route('/teacher/update/<int:selected_teacher_id>', methods=['GET', 'POST'])
def teacher_update(selected_teacher_id):

	student = teacher_select2(selected_teacher_id)
		
	teacher = Teacher.query.get_or_404(selected_teacher_id)
	#print("In PPPPPPPPPPPPTeacher UUUUUUUUUUUUUUUUUUUUUUpdate")
	#print(selected_teacher_id, teacher.id, teacher.first_name)
	
	if request.method == 'GET':
		#print("GET render update_teacher.html")
		return render_template('update_teacher.html', teacher=teacher)
  
	#get data from form and insert to teacher in teachergress  db
	#teacher.id = request.form.get('id')    #not updateable the field apears disabled for user 
	teacher.first_name = request.form.get('first_name')
	teacher.last_name = request.form.get('last_name')
	teacher.profetional = request.form.get('profetional')
	teacher.email = request.form.get('email')
	
	#db.session.update(teacher)	
	db.session.commit()  
	db.session.refresh(teacher)
	# test insert res
	url = url_for('teachers.edit_teachers')
	return redirect(url)   	
	return redirect(url_for('index'))
	
		
@tchr.route('/teacher/delete/', methods=['GET', 'POST'])
@login_required
def teacher_delete():
	  
	#print("RRRRRRRRRRRRRRRRRRRRRRRRRR")
	#print(current_user.id)

	user = User.query.get_or_404(current_user.id)
	author_id = user.id
	
	teacher = Teacher.query.filter(Teacher.selected==True).first()
	if teacher == None:
		flash("Please select a teacher to delete first ")
		return redirect(url_for('select.teacher_select'))
			
	teacher.hide = True
	db.session.commit()  

	return redirect(url_for('teachers.index')) 
		
#delete from index teachers list
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@tchr.route('/teacher/delete2/<int:selected_teacher_id>', methods=['GET', 'POST'])
@login_required
def teacher_delete2(selected_teacher_id):

	#print ("SSSSSSSSSSSSSelected teacher is", selected_teacher_id )
	student = teacher_select2(selected_teacher_id)
	#print(" IN teacher_delete2 dddddddddeleting teacher :", student.id)
	return teacher_delete()

	
	
##############teachers students###############	
@tchr.route('/students_by_teacher_show')
@login_required
def students_by_teacher_show():
	#print(" IN students_by_teacher_show")
	teacher = Teacher.query.filter(Teacher.selected==True).first()
	if teacher == None:
		flash("Please select a teacher first ")
		return redirect(url_for('select.teacher_select'))
	students = Student.query.join(Role).filter(Student.hide==False).filter(Role.teacher_id==teacher.id).filter(Role.student_id==Student.id).all()
	
	students_not_in_team = Student.query.join(Role).filter(Student.hide==False).filter(Role.teacher_id!=teacher.id).filter(Role.student_id==Student.id).all()

		
	teacher_team_students = Student.query.join(Role).filter(Student.hide==False).filter(Role.teacher_id==teacher.id).filter(Role.student_id==Student.id).all()	
	students_not_in_team = Student.query.join(Role).filter(Student.hide==False).filter(Role.teacher_id!=teacher.id).filter(Role.student_id==Student.id).all()

	return render_template('edit_teacher_students.html',
							teacher=teacher,
							teacher_team_students=teacher_team_students,
							students_not_in_team=students_not_in_team
							)

	
@tchr.route('/students_by_teacher_show2/<int:selected_teacher_id>', methods=['GET', 'POST'])
@login_required
def students_by_teacher_show2(selected_teacher_id):
	#print(selected_teacher_id)
	student = teacher_select2(selected_teacher_id)
	return redirect(url_for('students_by_teacher_show'))
							

@tchr.route('/edit_teacher_students', methods=['GET', 'POST'])
@login_required
def edit_teacher_students():
	
	teacher = Teacher.query.filter(Teacher.selected==True).first()
	if teacher == None:
		flash("Please select a teacher first ")
		return redirect(url_for('select.teacher_select'))
	
	teacher_team_students = get_teacher_students()
	students_not_in_team = get_students_not_of_teacher()
	
	print("In edit_teacher_students befor render edit_teacher_students teacher_team_students= :", teacher_team_students)
	#DEBUG
	for std in teacher_team_students:
		print("student: ", std.id)
		for r in std.teachers:
			print("Role is:  student is     teacher is role is ", r.student_id, r.teacher_id, r.title)
	#DEBUG
	
	accupations = Accupation.query.filter(Accupation.hide == False).all()	
	return render_template('edit_teacher_students.html',    teacher=teacher, 
														    teacher_team_students=teacher_team_students,
															accupations=accupations)



@tchr.route('/edit_teacher_students2/edit/<int:selected_teacher_id>/<int:selected_student_id>', methods=['GET', 'POST'])
@login_required
def edit_teacher_students2(selected_teacher_id, selected_student_id):
	print("In edit_teacher_students2 Request is :", request)
	teacher = teacher_select2(selected_teacher_id)
	if selected_student_id != 0:
		student = student_select2(selected_student_id)
	return edit_teacher_students()
 
 
@tchr.route('/student_to_teacher_add', methods=['GET', 'POST'])
@login_required
def student_to_teacher_add():
	print("IN Student_to_Teacher_add")
	##import pdb; pdb.set_trace()
	teacher = Teacher.query.filter(Teacher.selected==True).first()
	if teacher == None:
		flash("Please select a Teacher first ")
		return redirect(url_for('students.teacher_select'))

	students_not_of_teacher = get_students_not_of_teacher()
	#DEBUG
	print("students_not_of_teacher")
	for s in students_not_of_teacher:
		print("t name = ", s.id)
	#DEBUG
	accupations = Accupation.query.filter(Accupation.hide == False).all()
	if request.method == 'GET':
		return render_template('edit_students_not_of_teacher.html', teacher=teacher, 
																	students_not_of_teacher=students_not_of_teacher,
																	accupations=accupations)
																																															
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a Student first ")
		return redirect(url_for('students.student_select'))
		
	exist_role = Role.query.filter(Role.teacher_id == teacher.id).filter(Role.student_id==student.id).count()
	sr = request.form.get('selected_role')
	
	print("exist_role:", exist_role)
	print("exist_role:   role title:", exist_role, sr, request.method)
	
	if exist_role == 0:   #new Role
		##import pdb; pdb.set_trace()
		role = Role(teacher.id, student.id, sr)
		role.student = student
		role.teacher = teacher
		teacher.students.append(role)			
		student.teachers.append(role)
		print ("Role NEW title   NEW Student    NEW Teacher  :", role.title, role.student, role.teacher)

	else:
		role = Role.query.filter(Role.teacher_id == teacher.id).filter(Role.student_id==student.id).first()   #update role
		print("Existing Role is", role)
		print ("Role OLD title for Teacher and Student :", role.title, role.teacher_id, role.student_id)
		role.title=sr		
		print ("Role NEW title   OLD Student    OLD Teacher  :", role.title, role.student, role.teacher)

	print("IIIIIIIIIIIIIIIIIIIIIIn updating role ",  role.teacher.id, role.student_id, role.title)
	

	#DEBUG
	role = Role.query.filter(Role.student_id == student.id).filter(Role.teacher_id==teacher.id).first() 	
	print("New Reole title is: Role Teacher is   Role Student is ", role.title, role.teacher, role.student)
	#DEBUG
	db.session.commit() 
	db.session.refresh(teacher)
	db.session.refresh(student)
	db.session.refresh(role)
	
	#print("Student_to_Teacher_add METHOD", request.method)
	return  redirect(url_for('teachers.edit_teacher_students')) 
		
@tchr.route('/student_to_teacher_add2/<int:selected_teacher_id>/<int:selected_student_id>', methods=['GET', 'POST'])
def student_to_teacher_add2(selected_teacher_id, selected_student_id):
	print(selected_teacher_id)
	teacher_select2(selected_teacher_id)
	#print(selected_teacher_id)
	if selected_student_id:
		student_select2(selected_student_id)
	return student_to_teacher_add()	

			
@tchr.route('/student_from_teacher_delete', methods=['GET', 'POST'])
@login_required
def student_from_teacher_delete():
	##import pdb; pdb.set_trace()
	teacher = Teacher.query.filter(Teacher.selected==True).first()
	if teacher == None:
		flash("Please select a teacher first ")
		return redirect(url_for('select.teacher_select'))

	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('select.student_select'))
		
	#print("SSSSSRRRRR IN teacher_from_student_delete   deleteing teacher %s from student %s :",teacher.id, student.id )			

	role = Role.query.filter(Role.teacher_id == teacher.id).filter(Role.student_id==student.id).first()   #update role
	if role:
		print ("deleting  ROLE  ", role)
		db.session.delete(role)
		db.session.commit()
   
	db.session.commit() 
	db.session.refresh(teacher)
	db.session.refresh(student)
	
	#DEBUG
	role = Role.query.filter(Role.teacher_id == teacher.id).filter(Role.student_id==student.id).first()   #update role
	if role:		
		print ("DELETED ROLE IS ", role.id)
	#DEBUG
	
	return  redirect(url_for('teachers.edit_teacher_students'))  #no change in teachers team students

		
@tchr.route('/student_from_teacher_delete2/delete/<int:selected_teacher_id>/<int:selected_student_id>', methods=['GET', 'POST'])
@login_required
def student_from_teacher_delete2(selected_teacher_id, selected_student_id):
	#print("In DDDDDDDDDDDD teacher_from_student_delete2")
	student = teacher_select2(selected_teacher_id)
	if selected_student_id:
		#print(selected_student_id)
		teacher = student_select2(selected_student_id)
	return  redirect(url_for('teachers.student_from_teacher_delete'))  

	
	
@tchr.route('/get_teacher_students', methods=['GET', 'POST'])
@login_required
def get_teacher_students():
	print("In get_teacher_students")
	teacher = Teacher.query.filter(Teacher.selected==True).first()
	if teacher == None:
		flash("Please select a teacher first ")
		return redirect(url_for('select.teacher_select'))
	
	#DEBUG
	##import pdb; pdb.set_trace()	
	all_students = Student.query.all()
	'''
	for t in all_students:
		#print("TEacher teachers list :", t.id, t.teachers)
	'''
	teacher_team_students = Student.query.join(Role).filter(Student.hide==False).filter(Role.teacher_id==teacher.id).filter(Role.student_id==Student.id).all()

	return teacher_team_students



@tchr.route('/get_students_not_of_teacher', methods=['GET', 'POST'])
@login_required
def get_students_not_of_teacher():
	print ("SNOTSNOTSNOT get_students_not_of_teacher")
	teacher = Teacher.query.filter(Teacher.selected==True).first()
	if teacher == None:
		flash("Please select a teacher first ")
		return redirect(url_for('select.teacher_select'))
	
	#DEBUG
	##import pdb; pdb.set_trace()	
	all_students = Student.query.all()
	#DEBUG
	for s in all_students:
		print("11111111111111111 Student all_students list :", s.id)
	#DEBU
	
	teacher_students_team = Student.query.join(Role).filter(Role.teacher_id==teacher.id).filter(Role.student_id==Student.id).all()
	#DEBUG
	for s in teacher_students_team:
		print("222222222222222 Student teacher_students_team list :", s.id)
	#DEBU
		
	students_with_no_teachers = Student.query.filter(~Student.teachers.any()).all()
	#DEBUG
	for s in students_with_no_teachers:
		print("3333333333333333 Student students_with_no_teachers list :", s.id)
	#DEBUG
	
	students_not_of_teachers = list(set(all_students).difference(set(teacher_students_team)))  #teachers_not_in_staff = all_teachers-student_staff_teachers
	#DEBUG
	for s in students_not_of_teachers:
		print("4444444444444444444444 Student students_not_of_teachers list :", s.id)
	#DEBUG
		
	students_not_of_teachers.extend(students_with_no_teachers)
	#DEBUG
	for s in students_not_of_teachers:
		print("5555555555555555555555 Student students_not_of_teachers list :", s.id)
	#DEBUG
		
	##import pdb; pdb.set_trace()

	return students_not_of_teachers
##############studets students###############	









	
