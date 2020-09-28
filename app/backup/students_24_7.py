from flask import render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, json
from flask_login import login_user, logout_user, current_user, login_required
#from flask_login import login_manager

from flask_login import LoginManager
from config import basedir
import config

from app import app, db
from .forms import LoginForm
from .team_members import team_member_select2

from .models import User, Student, Team_member, Profile, Strength, Weaknesse, Role

from .forms import LoginForm, EditForm

from sqlalchemy import update

from .content_management import Content

from sqlalchemy import text # for execute SQL raw SELECT ...

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():

	g.user.__repr__()
	print("g sijax is")
	print(g.sijax).__repr__()

	students = Student.query.all()
	print("SSSSSSSSSSSSSSSSSSSSSSSStdnts")
	print (students)
	'''	
	return render_template('show_students2.html',
	user=g.user,
	students=students
	)
	'''
	return render_template('form6.html',)
	
	
@app.route('/show_student_tree', methods=['GET', 'POST'])
def show_student_tree():

	student = Student.query.filter(Student.selected==True).first()
	
	if student == None:
		flash("Please select a student to delete first ")
		return redirect(url_for('student_select'))
	print ("ttry selected student is " )

	print(student.first_name)	
	return render_template('lv.html', student=student)

					
@app.route('/show_student_tree2/<int:selected_student_id>', methods=['GET', 'POST'])
def show_student_tree2(selected_student_id):
	print ("SSSSSSSSSSSSSelected student is" )
	student_select2(selected_student_id)
	return show_student_tree()

	
@app.route('/students')
@login_required
def show_students():
	print ("in i0ndex show_students printing g.user ")
	students = Student.query.all()
	for student in students:
		print(student.first_name)
	
	return render_template('show_students3.html',
							students=students
							)


@app.route('/team_members_by_student_show')
@login_required
def team_members_by_student_show():
	print(" IN team_members_by_student_show")
	student = Student.query.filter(Student.selected==True).first()

	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('student_select'))
		
	team_members = team_members_by_student_get()
	for t in team_members:
		print("IN team_members_by_student_show team member:")
		print(t.first_name)
	return render_template('edit_student_staff_team.html',
							student=student,
							team_members=team_members,
							)

	
@app.route('/team_members_by_student_show2/<int:selected_student_id>', methods=['GET', 'POST'])
def team_members_by_student_show2(selected_student_id):
	print(selected_student_id)
	student_select2(selected_student_id)
	return redirect(url_for('team_members_by_student_show'))
							
@app.route('/team_members_by_student_get', methods=['POST', 'GET'])
@login_required
def team_members_by_student_get():
	print('IIIIIIIIIIIIIn team_member by student get')	
	student = Student.query.filter(Student.selected==True).first()

	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('student_select'))
		
	print("student")
	print(student.first_name)
	
	student_staff_members = Team_member.query.join(Team_member.clients).filter(Student.id==student.id).all()
	
	print("SSSSSSSSSSSStudents TTTTTTTTTTTTTTTTeam")
	for s in student_staff_members:
		print(s.first_name)
		
	return student_staff_members

	
@app.route('/team_members_by_student_and_role_get/<role>', methods=['POST', 'GET'])
@login_required
def team_members_by_student_and_role_get(role):
	print('IIIIIIIIIIIIIn team_member by student get')	
	student = Student.query.filter(Student.selected==True).first()

	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('student_select'))
		
	print("student")
	print(student.first_name)
	
	student_staff_members = Team_member.query.join(Team_member.clients).join(Team_member.clients.roles).filter(Student.id==student.id).filter(Team_member.clients.roles.title==role).all()
	
	print("SSSSSSSSSSSStudents TTTTTTTTTTTTTTTTeam")
	for s in student_staff_members:
		print(s.first_name)
		
	return student_staff_members

@app.route('/edit_student_staff_team', methods=['GET', 'POST'])
def edit_student_staff_team():
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('student_select'))
	
	
	#DEBUG
	print("DDDDDDDDDDDDDDDDDDDDDDebuging")
	ttt = Team_member.query.all()
	for t in ttt:
		print(t)
		print("Team member:",t.id)
		print("Team member clients len itself:", len(t.clients), t.clients)
		for c in t.clients:
			print("Team member's student:", student.id)
			print("members roles:", c.roles)
		for r in t.roles:
			print(r)			
			print("role: std mem role", r.student_id, r.team_member_id, r.title)
			
		#do_not_have_students = Team_member.query.join(Team_member.clients).filter(~Team_member.clients.any()).all()
		do_not_have_students = Team_member.query.filter(
		print("do_not_have_students", do_not_have_students)
	#import pdb; pdb.set_trace()
	q = Student.query.join(Team_member).filter(Team_member.clients.any())
	
	

	#DEBUG
	
	
	
	student_staff_members = Team_member.query.join(Student.staff_team_members).filter(Student.id==student.id).all()
	exist_member = False
	for s in student_staff_members:
		exist_member = True
	import pdb; pdb.set_trace()
	if exist_member == False: # retrieve all team members for  team_members_not_in_staff scince student doesn't have ant team member in his staff		
		team_members_not_in_staff = Team_member.query.all() 
	else:
		team_members_not_in_staff_number_n = Team_member.query.join(Team_member.clients).filter(Student.id!=student.id).count() 
		if team_members_not_in_staff_number_n == 0:    #Team members have no students
			team_members_not_in_staff = Team_member.query.join(Team_member.clients).filter(Team_member.clients is None)
		else:
			team_members_not_in_staff = Team_member.query.join(Team_member.clients).filter(Student.id!=student.id).all()
			
	if request.method == 'GET':
		return render_template('edit_student_staff_team.html', student=student, 
															   student_staff_members=student_staff_members,
															   team_members_not_in_staff=team_members_not_in_staff)															
	else:	
		print("in else calling team_members_by_student_show")
		return  redirect(url_for('team_members_by_student_show'))  #no change in students staff members
		
		
		
@app.route('/edit_student_staff_team2/edit/<int:selected_student_id>/<int:selected_team_member_id>', methods=['GET', 'POST'])
def edit_student_staff_team2(selected_student_id, selected_team_member_id):
	print(selected_student_id)
	student_select2(selected_student_id)
	if selected_team_member_id != 0:
		print(selected_team_member_id)
		student_select2(selected_team_member_id)
	return edit_student_staff_team()
 
 
@app.route('/student_staff_member_add', methods=['GET', 'POST'])
def student_staff_member_add():

	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('student_select'))

	team_member = Team_member.query.filter(Team_member.selected==True).first()
	if team_member == None:
		flash("Please select a team_member first ")
		return redirect(url_for('team_member_select'))
		
	print("SSSSSRRRRR IN student_staff_member_add")		
	print(student.id)
	print(team_member.id)		
	#Check If This team member exist (have Role)  for this student
	exist_role = Role.query.filter(Role.student_id == student.id).filter(Role.team_member_id==team_member.id).count()
	
	print("exist_role:", exist_role)

	if exist_role == 0:   #new Role
		role = Role(student.id, team_member.id)
	else:
		role = Role.query.filter(Role.student_id == student.id).filter(Role.team_member_id==team_member.id)
		
	sr = request.form.get('selected_role')
	role.title = sr
	print("IIIIIIIIIn student_staff_member_add ", role.student_id, role.team_member_id, role.title)
	
	if exist_role == 0:	#New Role - should be appended to roles list	
		student.staff_team_members.append(team_member)	
		student.roles.append(role)
		
		team_member.clients.append(student)   
		team_member.roles.append(role)  
	   
	db.session.commit() 
	
	url = url_for('edit_student_staff_team')
	return redirect(url)
   	
@app.route('/student_staff_member_add2/add/<int:selected_student_id>/<int:selected_team_member_id>', methods=['GET', 'POST'])
def student_staff_member_add2(selected_student_id, selected_team_member_id):
	print("IIIIIIIIIIIIIIIn student_staff_member_add222 view")
	print(request.form.get('selected_role'))
	
	print(selected_student_id)
	student_select2(selected_student_id)
	
	print(selected_team_member_id)
	team_member_select2(selected_team_member_id)
	
	return student_staff_member_add()

	
@app.route('/student_staff_member_delete', methods=['GET', 'POST'])
def student_staff_member_delete():

	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('student_select'))
	
	team_member = Team_member.query.filter(Team_member.selected==True).first()
	if team_member == None:
		flash("Please select a team_member first ")
		return redirect(url_for('team_member_select'))
		
	##import pdb; pdb.set_trace()
	staff_member = Team_member.query.join(Student.staff_team_members).filter(Student.staff_team_members.id==team_member.id)
	s_role = Role.query.join(Student.roles).filter(Student.roles.team_member_id==team_member.id and Student.roles.student_id==student.id)

	student.staff_team_members.delete(staff_member)   
	student.roles.delete(s_role)  	

	client = Student.query.join(Team_member.clients).filter(Team_member.clients.id==student.id)
	role = Role.query.join(Team_member.roles).filter(Team_member.roles.team_member_id==team_member.id) #checking for debug
	t_role = Role.query.join(Team_member.roles).filter(Team_member.roles.team_member_id==team_member.id and Team_member.roles.student_id==student.id)	
	
	team_member.clients.delete(client)   
	team_member.roles.delete(t_role)  
	   
	db.session.commit() 
	
	url = url_for('team_members_by_student_show')
	return redirect(url)
   	
@app.route('/student_staff_member_delete2/add/<int:selected_student_id>/<int:selected_team_member_id>', methods=['GET', 'POST'])
def student_staff_member_delete2(selected_student_id, selected_team_member_id):
	print(selected_student_id)
	student_select2(selected_student_id)
	if selected_team_member_id:
		print(selected_team_member_id)
		student_select2(selected_team_member_id)
	return student_staff_member_add2()


	
#Select a student from a list 
@app.route('/student_select', methods=['GET', 'POST'])
def student_select():
	print("1111111111111")
	students = Student.query.all()
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
	students = Student.query.all()
	#return render_template('show_selected_student.html', students=students)
	return show_students()

	
#Select a student from a list 
@app.route('/student_select2/<int:selected_student_id>', methods=['GET', 'POST'])
def student_select2(selected_student_id):
	print("in student_select22222222222222222222222222222")
	
	students = Student.query.all()
	for student in students:
		student.selected = False

	student = Student.query.get_or_404(selected_student_id)		
		
	student.selected = True
	print(student.first_name)
	
	db.session.commit()
	
	student = Student.query.get_or_404(selected_student_id)
	print(student.selected)
	students = Student.query.all()
	return render_template('show_selected_student.html', students=students)
	
	#Select a student from a list 
	
			   
@app.route('/student/add/', methods=['GET', 'POST'])
#Here author is user_id
def student_add():
	  
	print("RRRRRRRRRRRRRRRRRRRRRRRRRR")
	user = User.query.get_or_404(g.user.id)
	print(g.user)

	#print request
	
	if request.method == 'GET':
		return render_template('add_student.html', user=user)
		   
	#get data from form and insert to student in studentgress  db
	id = request.form.get('id')
	first_name = request.form.get('first_name')
	last_name = request.form.get('last_name')
	birth_date = request.form.get('birth_date')
	grade = request.form.get('grade')
	
	#import pdb; pdb.set_trace() 	
	student = Student(id, first_name, last_name, birth_date, grade)	
	
	db.session.add(student)	
	db.session.commit()  
	db.session.refresh(student)
	# test insert res
	url = url_for('show_students')
	return redirect(url)   


	
#update selected student
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@app.route('/student/update/<int:selected_student_id>', methods=['GET', 'POST'])
def student_update(selected_student_id):

	student_select2(selected_student_id)
		
	student = Student.query.get_or_404(selected_student_id)
	print("In PPPPPPPPPPPPStudent UUUUUUUUUUUUUUUUUUUUUUpdate")
	print(selected_student_id, student.id, student.first_name)
	
	if request.method == 'GET':
		print("GET render update_student.html")
		return render_template('update_student.html', student=student)
		
	#get data from form and insert to studentgress db
	##import pdb; pdb.set_trace() 	
	student.first_name = request.form.get('first_name')	
	student.body = request.form.get('description')
	
	db.session.commit()  
	db.session.refresh(student)
	
	return redirect(url_for('index'))
	
		
@app.route('/student/delete/', methods=['GET', 'POST'])
#Here author is user_id
def student_delete():
	  
	print("RRRRRRRRRRRRRRRRRRRRRRRRRR")
	print(g.user)

	user = User.query.get_or_404(g.user.id)
	author_id = user.id
	
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student to delete first ")
		return redirect(url_for('student_select'))
			
	print ("delete selected student is " )
	print(student.first_name)	  

	profiles = Profile.query.join(Student.profiles).filter(Student.id==student.id)
	for profile in profiles:
		profile_delete2(profile.id)		
		
	db.session.delete(student) 
	
	db.session.commit()  

	return redirect(url_for('index')) 
		
#delete from index students list
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@app.route('/student/delete2/<int:selected_student_id>', methods=['GET', 'POST'])
#Here author is user_id
def student_delete2(selected_student_id):

	print ("SSSSSSSSSSSSSelected student is" )
	student_select2(selected_student_id)
	return student_delete()












	
