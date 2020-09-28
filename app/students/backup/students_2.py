from flask import render_template, flash, redirect
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
from app.select.select import std_general_txt_select2, general_txt_select2, specific_gt_type_select2, gt_type_select2
from app.select.select import destination_select2, goal_select2, todo_select2, std_goal_select2, document_select2
from app.select.select import profile_select2, strength_select2, subject_select2, weakness_select2
from app.select.select import age_range_select2, tag_select2, sub_tag_select2

from app.gts.gts import get_categories_of, set_gt_category, get_default_child, get_color

# from app.profile.profile import get_default_prf


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
from app import *

@std.route('/')
@std.route('/index', methods=['GET', 'POST'])
@login_required
def index():

    #Reset student selection
    students = Student.query.all()
    for std in students:
        std.selected = False
    db.session.commit() 

    students = Student.query.filter(Student.hide == False).all()

    return render_template('try_img_ratio.html')

@std.route('/student_home' )
@login_required
def student_home():
	return render_template('try_img_ratio.html')
	    
@std.route('/get_author_id', methods=['GET', 'POST'])
@login_required
def get_author_id():
    return current_user._get_current_object().id

            
@std.route('/show_student_tree', methods=['GET', 'POST'])
@login_required
def show_student_tree():

    ############################import pdb;; #pdb.set_trace()
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))
      
    std_gts = General_txt.query.join(Std_general_txt).filter(Std_general_txt.student_id==std.id).filter(Std_general_txt.general_txt_id==General_txt.id).all()
        
    student_dsts = []    # Get all student's destinations
    all_dsts = Destination.query.filter(Destination.hide==False).all()  
    for d in all_dsts:
        std_dst = Std_general_txt.query.filter(Std_general_txt.student_id==std.id).filter(Std_general_txt.general_txt_id==d.id).first()
        if std_dst !=None:
           student_dsts.append(d)            
    #destinations_not_of_student = list(set(all_dsts).difference(set(student_dsts)))  #destinations_not_of_student = all_destinations - std_destinations
   
    student_goals = []    # Get all student's destinations
    all_goals = Goal.query.filter(Goal.hide==False).all()
   
  
    for g in std_gts:
        if g in all_goals:
            student_goals.append(g)
    #goals_not_of_student = list(set(all_goals).difference(set(student_goals)))  #goals_not_of_student = all_destinations - std_destinations
    
                                  
    student_todos = []    # Get all student's destinations
    all_todos = Todo.query.filter(Todo.hide==False).all()
    
    for g in std_gts:
        if g in all_todos:
            student_todos.append(g)
    #todos_not_of_student = list(set(all_todos).difference(set(student_todos)))  #todos_not_of_student = all_destinations - std_destinations


    #DEBUG ONLY
    for d in student_dsts:
        print("D", d.title, d.id)
        for g in student_goals: 
            if d.is_parent_of(g):
                print("   G", g.title, g.id)
            for t in student_todos:
                if g.is_parent_of(t):
                    print("         G  T", g.id,  t.id)
    #DEBUG ONLY
    
        
    whos = Accupation.query.all()
    default_who = Accupation.query.filter(Status.default==True).first()

    statuss = Status.query.all()
    default_status = Status.query.filter(Status.default==True).first()
        
    whos = Accupation.query.all()
    default_who = Accupation.query.filter(Accupation.default==True).first()

    tags = Tag.query.all()
    
    std_txts = Std_general_txt.query.filter(Std_general_txt.student_id==std.id).all()
     
    due_date = date.today()
        
    age_ranges = Age_range.query.order_by(Age_range.title).all()
    tags = Tag.query.order_by(Tag.title).all()

    return render_template('./tree/show_student_tree.js', std=std, student=std,  
                                                        student_dsts=student_dsts,
                                                        student_goals=student_goals,
                                                        student_todos=student_todos,
                                                        total_gts = len(student_dsts)+len(student_goals)+len(student_todos),
                                                        std_txts=std_txts,
                                                        statuss=statuss,
                                                        whos=whos,
                                                        tags=tags, 
                                                        age_ranges=age_ranges,
                                                        due_date=due_date)			
               
    
    
@std.route('/show_student_tree2/<int:selected_student_id>', methods=['GET', 'POST'])
@login_required
def show_student_tree2(selected_student_id):
    std = student_select2(selected_student_id)
    return redirect(url_for('students.show_student_tree'))

	
@std.route('/edit_students')
@login_required
def edit_students():
    students = Student.query.filter(Student.hide==False).all()
    return render_template('edit_students3.html',
                            students=students
                            )
							
							
@std.route('/get_dummy_student', methods=['GET', 'POST'])
def get_dummy_student():
	dummy_std = Student.query.filter(Student.id==0).first()
	if dummy_std:
		return dummy_std
	else:
		dummy_std = Student(0, 'Humpty', 'Dumpty', date.today(), 'D', get_author_id())
		dummy_std.hide=True
		db.session.add(dummy_std)	
		db.session.commit()  
		db.session.refresh(dummy_std)
	return dummy_std
								
@std.route('/student_add', methods=['GET', 'POST'])
@login_required
def student_add():
      
    author_id = User.query.get_or_404( current_user._get_current_object().id)

    if request.method == 'GET':
        return render_template('add_student.html', author_id=author_id)
           
    #get data from form and insert to student in studentgress  db
    id = request.form.get('id')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    birth_date = request.form.get('birth_date')
    grade = request.form.get('grade')
    background = request.form.get('background')

    student_already_exist = Student.query.filter(Student.id == id).first()
    if student_already_exist is not None :  #Student already exist in system probably in hide mode
        flash("This student already exists in system", student_already_exist.id)
        return render_template('un_hide_student.html', student_already_exist=student_already_exist)

    std = Student(id, first_name, last_name, birth_date, grade, author_id.id)	    
    db.session.add(std)	
    db.session.commit() 	
  
    std.background = background
    
    #FROM https://stackoverflow.com/questions/25189017/tablemodel-inheritance-with-flask-sqlalchemy
    new_profile = Profile(title=std.first_name + 's Profile', body=str(std.id), author_id=author_id.id)

    db.session.add(new_profile)	
    db.session.commit() 	
    
    attach_gt_to_std(std.id, new_profile.id)

    db.session.add(std)	
    db.session.commit()  
    db.session.refresh(std)

    url = url_for('students.edit_students')
    return redirect(url)   


@std.route('/student_unhide2/<int:selected_student_id>', methods=['GET', 'POST'])
#Here author is user_id
@login_required
def student_unhide2(selected_student_id):
	  
	user = User.query.get_or_404(current_user._get_current_object().id)

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

	std = student_select2(selected_student_id)
	return student_delete()



@std.route('/student_delete_for_good', methods=['GET', 'POST'])
#Here author is user_id
@login_required
def student_delete_for_good():

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

	std = student_select2(selected_student_id)
	return student_delete_for_good()
    
        
##############START studets plan report###############
	
@std.route('/plan_report', methods=['GET', 'POST'])
@login_required
def plan_report():
	
    print("IN PLAN REPORT ")
    print("")
    
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))
      
    std_gts = General_txt.query.join(Std_general_txt).filter(Std_general_txt.student_id==std.id).filter(Std_general_txt.general_txt_id==General_txt.id).all()
    
    print("std_gts", std_gts)
    print("")
    
    student_dsts = []    # Get all student's destinations
    all_dsts = Destination.query.filter(Destination.hide==False).all()  
    for d in all_dsts:
        std_dst = Std_general_txt.query.filter(Std_general_txt.student_id==std.id).filter(Std_general_txt.general_txt_id==d.id).first()
        if std_dst !=None:
            student_dsts.append(d) 
            for c in d.children:
                if c not in std_gts:
                    std_gts.append(c)
    
    print("student_dsts", student_dsts)
    print("")
    print("")
    
    destinations_not_of_student = list(set(all_dsts).difference(set(student_dsts)))  #destinations_not_of_student = all_destinations - std_destinations
   
    
    student_goals = []    # Get all student's destinations
    all_goals = Goal.query.filter(Goal.hide==False).all()
    for g in std_gts:
        if g in all_goals:
            student_goals.append(g)
            for c in d.children:
                if c not in std_gts:
                    std_gts.append(c)    
    goals_not_of_student = list(set(all_goals).difference(set(student_goals)))  #goals_not_of_student = all_destinations - std_destinations
                                 
    student_todos = []    # Get all student's destinations
    all_todos = Todo.query.filter(Todo.hide==False).all()
    for g in std_gts:
        if g in all_todos:
            student_todos.append(g)
            for c in d.children:
                if c not in std_gts:
                    std_gts.append(c)    
    todos_not_of_student = list(set(all_todos).difference(set(student_todos)))  #todos_not_of_student = all_destinations - std_destinations
      
    whos = Accupation.query.all()
    default_who = Accupation.query.filter(Status.default==True).first()

    statuss = Status.query.all()
    default_status = Status.query.filter(Status.default==True).first()
        
    whos = Accupation.query.all()
    default_who = Accupation.query.filter(Accupation.default==True).first()

    tags = Tag.query.all()
    
    std_txts = Std_general_txt.query.filter(Std_general_txt.student_id==std.id).all()


    due_date = date.today()
   
    age_ranges = Age_range.query.order_by(Age_range.title).all()
    tags = Tag.query.order_by(Tag.title).all()

    student_staff_teachers = get_student_teachers()
    
    #PROFILE
    
    profile = get_std_gt(std.id, 'Profile')   
        
    prf_subjects=[]
    all_subjects = Subject.query.all()
    for s in all_subjects:
        if profile.is_parent_of(s):
            prf_subjects.append(s)
        
    prf_weaknesses=[]
    all_weaknesses = Weakness.query.all()
    for s in all_weaknesses:
        if profile.is_parent_of(s):
            prf_weaknesses.append(s)
        
    prf_strengths=[]
    all_strengths = Strength.query.all()
    for s in all_strengths:
        if profile.is_parent_of(s):
            prf_strengths.append(s)
 
    #PROFILE

    tags = Tag.query.order_by(Tag.title).all()
    sub_tags = Sub_tag.query.order_by(Sub_tag.title).all()
    
    author_id = get_author_id()
    sbj = Subject.query.filter(Subject.title=='Subject_data').first()
    if sbj==None:
        sbj = Subject('Subject_data', 'Subject_data', author_id)
    

    strn = Strength.query.filter(Strength.title=='Subject_data').first()
    if strn==None:
        strn = Strength('Strength_data', 'Strength_data', author_id)
    
    print("")
    print("")
    print("STRN ODD: ", strn.odd_color)
    print("STRN EVEN: ", strn.even_color)
    print("")
    print("")
    
    weak = Weakness.query.filter(Weakness.title=='Subject_data').first()
    if weak==None:
        weak = Weakness('Weakness', 'Weakness', author_id)
    

            
    return render_template('plan_report/plan_report.html', 
                                                        std=std, student=std, std_gts=std_gts,
                                                        student_dsts=student_dsts, destinations_not_of_student=destinations_not_of_student,
                                                        all_goals=all_goals, student_goals=student_goals, goals_not_of_student=goals_not_of_student,
                                                        all_todos=all_todos, student_todos=student_todos, todos_not_of_student=todos_not_of_student,
                                                        std_txts=std_txts,
                                                        statuss=statuss, default_status=default_status,
                                                        whos=whos, default_who=default_who,
                                                        tags=tags, sub_tags=sub_tags, age_ranges=age_ranges, 
                                                        due_date=due_date,
                                                        student_staff_teachers=student_staff_teachers,
                                                        profile=profile, prf_subjects=prf_subjects, prf_strengths=prf_strengths, prf_weaknesses=prf_weaknesses,
                                                        sbj=sbj, strn=strn, weak=weak )  

@std.route('/plan_report2/<int:selected_student_id>', methods=['GET', 'POST'])
@login_required
def plan_report2(selected_student_id):
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
	accupations = Accupation.query.filter(Accupation.hide == False).all()
	return render_template('./teachers/edit_student_teachers.html',   student=student, 
														   student_staff_teachers=student_staff_teachers,
														   accupations=accupations)
														   		
														  		
@std.route('/edit_student_teachers2/<int:selected_student_id>/<int:selected_teacher_id>', methods=['GET', 'POST'])
@login_required
def edit_student_teachers2(selected_student_id, selected_teacher_id):
	std = student_select2(selected_student_id)
	if selected_teacher_id != 0:
		tchr = teacher_select2(selected_teacher_id)
	return edit_student_teachers()
 
 
@std.route('/teacher_to_student_add', methods=['GET', 'POST'])
@login_required
def teacher_to_student_add():

	###########################impor pdb;#pdb.set_trace()
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
    
	if exist_role == 0:   #new Role
		###########################impor pdb;#pdb.set_trace()
		role = Role(student.id, teacher.id, sr)
		role.teacher = teacher
		role.student = student
		student.teachers.append(role)			
		teacher.students.append(role)

	else:
		role = Role.query.filter(Role.student_id == student.id).filter(Role.teacher_id==teacher.id).first()   #update role
		role.title=sr		

	#DEBUG
	role = Role.query.filter(Role.teacher_id == teacher.id).filter(Role.student_id==student.id).first() 	
	#DEBUG
	db.session.commit() 
	db.session.refresh(student)
	db.session.refresh(teacher)
	db.session.refresh(role)
	
	return  redirect(url_for('students.edit_student_teachers')) 
		
		
	
@std.route('/teacher_to_student_add2/<int:selected_teacher_id>/<int:selected_student_id>', methods=['GET', 'POST'])
@login_required
def teacher_to_student_add2(selected_teacher_id, selected_student_id):
	student_select2(selected_student_id)
	if selected_teacher_id:
		teacher_select2(selected_teacher_id)
	return teacher_to_student_add()
    
		
@std.route('/teacher_from_student_delete', methods=['GET', 'POST'])
@login_required
def teacher_from_student_delete():
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('students.edit_students'))

	teacher = Teacher.query.filter(Teacher.selected==True).first()
	if teacher == None:
		flash("Please select a teacher first ")
		return redirect(url_for('select.teacher_select'))
		
	role = Role.query.filter(Role.student_id == student.id).filter(Role.teacher_id==teacher.id).first()   #update role
	if role:	
		db.session.delete(role)
		db.session.commit()
	
	return  redirect(url_for('students.edit_student_teachers'))  #no change in students staff teachers
		
@std.route('/teacher_from_student_delete2/delete/<int:selected_teacher_id>/<int:selected_student_id>', methods=['GET', 'POST'])
@login_required
def teacher_from_student_delete2(selected_teacher_id, selected_student_id):
	std = student_select2(selected_student_id)
	if selected_teacher_id:
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
	
	all_teachers = Teacher.query.all()

	student_staff_teachers = Teacher.query.join(Role).filter(Role.student_id==student.id).filter(Role.teacher_id==Teacher.id).all()
	
	teachers_with_no_students = Teacher.query.filter(~Teacher.students.any()).all()
	
	teachers_not_in_staff = list(set(all_teachers).difference(set(student_staff_teachers)))  #teachers_not_in_staff = all_teachers-student_staff_teachers
	
	teachers_not_in_staff.extend(teachers_with_no_students)


	return teachers_not_in_staff
##############studets teachers###############	



##############studets destinations###############	
@std.route('/edit_student_destinations', methods=['GET', 'POST'])
@login_required
def edit_student_destinations():
    
    default_tag = Tag.query.filter(Tag.selected==True).first()
    default_ar = Age_range.query.filter(Age_range.selected==True).first()
    
    return student_dsts()



#FROM https://stackoverflow.com/questions/55736527/how-can-i-yield-a-template-over-another-in-flask
from flask import stream_with_context, Response
import time
from time import sleep

																									  		
@std.route('/edit_student_destinations2/edit/<int:selected_student_id>/<int:selected_destination_id>', methods=['GET', 'POST'])
@login_required
def edit_student_destinations2(selected_student_id, selected_destination_id):

    std = student_select2(selected_student_id)
    if selected_destination_id != 0:
        dest = destination_select2(selected_destination_id)
    #return redirect(url_for('students.edit_student_destinations', ))		
    return edit_student_destinations()		


@std.route('/update_student_age_range_for_edit_destination/edit/<int:selected_student_id>', methods=['GET', 'POST'])
@login_required
def update_student_age_range_for_edit_destination(selected_student_id):
    std = student_select2(selected_student_id)
    student = Student.query.filter(Student.selected==True).first()

    ar_title = request.form.get('selected_age_range')
    ar = Age_range.query.filter(Age_range.title == ar_title).first()
    age_ranges = Age_range.query.all();
    return render_template('./destinations/edit_student_destinations.html', student=student, age_ranges=age_ranges, default_age_range = ar)

@std.route('/update_student_scrt_for_edit_destination/edit/<int:selected_student_id>', methods=['GET', 'POST'])
@login_required
def update_student_scrt_for_edit_destination(selected_student_id):
    std = student_select2(selected_student_id)
    student = Student.query.filter(Student.selected==True).first()

    scrt_title = request.form.get('selected_age_range')
    scrt = Scrt.query.filter(Scrt.title == scrt_title).first()
    scrts = Scrt.query.all();
    return render_template('edit_student_destinations.html', student=student, scrts=scrts)


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
  
    all_destinations = Destination.query.filter(Destination.hide==False).filter(Destination.hide==False).all()
    std_destinations = Destination.query.join(Std_general_txt).filter(Std_general_txt.general_txt_id==Destination.id).filter(Std_general_txt.student_id == std.id).all()		
    destinations_not_of_student = list(set(all_destinations).difference(set(std_destinations)))  #students_not_in_staff = all_students - std_destinations
        
    age_ranges = Age_range.query.all()
    tags = Tag.query.all() 

    if request.method == 'GET':
                                                                
        return render_template('./destinations/edit_destinations_not_of_student.html',
                                                                std=std,
                                                                destinations=destinations_not_of_student, 
                                                                age_ranges=age_ranges,
                                                                tags=tags)

@std.route('/destination_to_student_add2/<int:selected_student_id>', methods=['GET', 'POST'])
@login_required
def destination_to_student_add2(selected_student_id):
	std = student_select2(selected_student_id)
	return redirect(url_for('students.destination_to_student_add')) 	
	


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
            
    std_dst = Std_general_txt.query.filter(Std_general_txt.student_id==student.id).filter(Std_general_txt.general_txt_id==destination.id).first()
    if std_dst != None:
        if std_dst in student.general_txts:
            student.general_txts.remove(std_dst)
        if std_dst in destination.students:            
            destination.students.remove(std_dst)
            
    db.session.commit()  

    return redirect(url_for('students.edit_student_destinations', )) 
    

@std.route('/destination_from_student_delete2/<int:selected_student_id>/<int:selected_destination_id>', methods=['GET', 'POST'])
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
    if dst == None:
        flash("Please select a destination first ")
        return redirect(url_for('students.edit_student_destinations', ))
            
    student_goals = []
    all_goals = Goal.query.all()  
    for g in all_goals:
        if g in dst.children:
           student_goals.append(g) 
    
    student_todos = []
    all_todos = Todo.query.all() 
    for g in student_goals:
        for t in all_todos:
            if t in g.children:
               student_todos.append(g) 
          

    statuss = Status.query.all()
    whos = Accupation.query.all()
    
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

    return edit_student_goals()
    
		
@std.route('/goal_from_student_delete', methods=['GET', 'POST'])
@login_required
def goal_from_student_delete():
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('students.edit_students'))

	goal = Goal.query.filter(Goal.selected==True).first()
	if goal == None:
		flash("Please select a goal first ")
		return redirect(url_for('select.goal_select'))
		
	std_goal = Std_goal.query.filter(Std_goal.student_id == student.id).filter(Std_goal.goal_id==goal.id).first()   #update std_goal
	if std_goal:	
		db.session.delete(std_goal)
		db.session.commit()
	
	return  redirect(url_for('students.edit_student_goals'))  #no change in students staff goals
		
@std.route('/goal_from_student_delete2/delete/<int:selected_goal_id>/<int:selected_student_id>', methods=['GET', 'POST'])
@login_required
def goal_from_student_delete2(selected_goal_id, selected_student_id):
	std = student_select2(selected_student_id)
	if selected_goal_id:
		goal = goal_select2(selected_goal_id)
	return  redirect(url_for('students.goal_from_student_delete'))  

##############studets goals###############		


	
##############START TRY studets goals###############	

@std.route('/try_goal_to_student_add', methods=['GET'])
@login_required
def try_goal_to_student_add():
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('destination.edit_students'))

    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_student_destinations', ))		
           
    goals_not_of_student = try_get_goals_not_of_student()
    if len(goals_not_of_student) < 1:
        flash("כל היעדים של מטרה זו כבר משוייכים לתלמיד. אפשר ליצור יעד חדש דרך  עריכת יעדים למטרה  ")
        redirect(url_for('students.edit_student_goals'))

    statuss = Status.query.all()
    due_date = date.today()
    
    student_goals = Std_goal.query.filter(Std_goal.student_id==std.id).filter(Std_goal.general_txt_id==dst.id).all()
 
    
    return render_template('./goals/edit_std_goals_and_std_not_of_std_goals.html', std=std, dst=dst, 
                                                                goals_not_of_student=goals_not_of_student,
                                                                statuss=statuss, due_date=due_date,
                                                                std_goals=student_goals)


################## START update_std_goal_form ################    
@std.route('/update_std_goal_form', methods=['GET', 'POST'])
@login_required
def update_std_goal_form():

    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('destination.edit_students'))

    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_student_destinations', ))		
   
    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('students.edit_student_goals'))
            
    updated_std_goal = Std_goal.query.filter(Std_goal.selected==True).first()
    if updated_std_goal == None:
        flash("Please select a student's goal to update")
        return redirect(url_for('students.edit_student_goals'))
            
    if updated_std_goal == None:   #Add a new Std_goal
        updated_std_goal = Std_goal(std.id, goal.id)
        std_goal = std_goal_select2(selected_goal_id, std.id) 
        updated_std_goal.goal_title = request.form.get('goal_id')
        updated_std_goal.goal_body =  request.form.get('goal_body')    
        updated_std_goal.goal = goal
        updated_std_goal.student = std    
        updated_std_goal.general_txt_id = dst.id
        std.goals.append(updated_std_goal)			
        goal.students.append(updated_std_goal)
        
    status = Status.query.filter(Status.id==request.form['status']).first()    
    updated_std_goal.status_id = status.id
    updated_std_goal.status_title = status.title
    updated_std_goal.status_color = status.color
    
    updated_std_goal.due_date = request.form.get('due_date') 
           
    goal.selected = False
    updated_std_goal.selected = False
    db.session.commit() 

    return  redirect(url_for('students.edit_student_goals')) 


@std.route('/update_std_goal_form2', methods=['GET', 'POST'])
@login_required
def update_std_goal_form2():
    selected_goal_id = request.form['goal_id']
    
    goal = goal_select2(selected_goal_id) 
    
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
        return redirect(url_for('students.edit_student_destinations', ))		
        

    student_goals = Goal.query.join(Std_goal).filter(Std_goal.general_txt_id==dst.id).filter(Std_goal.student_id==std.id).all()

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
        return redirect(url_for('students.edit_student_destinations', ))		

    #DEBUG
    all_dst_goals = Goal.query.join(Destination).filter(Goal.general_txt_id == dst.id)

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
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a goal first ")
        return redirect(url_for('students.edit_students'))		
    
    std_goal = Std_goal.query.filter(Std_goal.selected==True).first()
    if std_goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('students.edit_student_goals'))	
        
    dst = Destination.query.filter(Destination.id==std_goal.general_txt_id).first()
    if dst == None:
        flash("Please select a destination for student first ")
        return redirect(url_for('students.edit_student_destinations'))		
   
   
    student_todos = Std_todo.query.filter(Std_todo.student_id==std_goal.student_id).filter(Std_todo.goal_id==std_goal.goal_id).all()
    
    
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
    std_goal = std_goal_select2(selected_std_id, selected_goal_id)

    return edit_student_todos()

														  		
@std.route('/get_std_todos', methods=['GET', 'POST'])
@login_required
def get_std_todos(std, std_goal, dst):
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a goal first ")
        return redirect(url_for('students.edit_students'))		
    
    std_goal = Std_goal.query.filter(Std_goal.selected==True).first()
    if std_goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('students.edit_student_goals'))	
        
    dst = Destination.query.filter(Destination.id==std_goal.general_txt_id).first()
    if dst == None:
        flash("Please select a destination for student first ")
        return redirect(url_for('students.edit_student_destinations'))		
   
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

    #### GET case
    todos_not_of_student = get_todos_not_of_student()
    
    
    if (todos_not_of_student == None) or (len(todos_not_of_student) < 1):
        flash("כל המשימות של יעדזה כבר משוייכות לתלמיד. אפשר ליצור משימה חדשה דרך יצירת מטרות-יעדים-משימות.")
        redirect(url_for('students.edit_student_todos'))

    statuss = Status.query.all()
    whos = Accupation.query.all()
    due_date = date.today()
    return render_template('./goals/todos/edit_todos_not_of_std.html', std=std, dst=dst, std_goal=std_goal,
                                                                todos_not_of_student=todos_not_of_student,
                                                                statuss=statuss, whos=whos, due_date=due_date)
                                                                
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
        

    student_todos = Todo.query.join(Std_todo).filter(Std_todo.general_txt_id==dst.id).filter(Std_todo.student_id==std.id).all()

    return student_todos


@std.route('/try_get_todos_not_of_student', methods=['GET', 'POST'])
@login_required
def try_get_todos_not_of_student():

    #############################import_pdb; #pdb.set_trace()
   
    student = Student.query.filter(Student.selected==True).first()
    if student == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))
    
    std_goal = Std_general_txt.query.filter(Std_general_txt.selected==True).filter(Std_general_txt.type=='goal').first()
    if std_goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('students.edit_student_goals'))		
            
    
    all_goal_todos = Todo.query.filter(Todo in std_goal.children)
    all_goal_todos = Todo.query.filter(Todo in std_goal.children)
    
    student_todos = Todo.query.filter(Todo in student.general_txts).all()

    todos_not_of_student = list(set(all_goal_todos).difference(set(student_todos)))  #todos_not_of_student = all_dst_goal-student_todos
  
    return todos_not_of_student



@std.route('/get_dst_todos_not_of_student', methods=['GET', 'POST'])
@login_required
def get_dst_todos_not_of_student():
           
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))

    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_student_goals'))
  
    all_dst_golas = Goal.query.filter(Goal in dst.children).all()
    all_dst_todos = []
    for g in all_dst_golas:
        g_todos = Todo.query.filter(Goal in g.children).all()
        for gt in g_todos:
            all_dst_todos.append(gt)
            
    student_todos = Std_general_txt.query.filter(Std_general_txt.student_id==std.id).filter(Std_general_txt.general_txt in all_dst_todos).all()

    todos_not_of_student = list(set(all_dst_todos).difference(set(student_todos)))  #todos_not_of_student = all_dst_goal-student_todos

    return todos_not_of_student


@std.route('/get_goal_todos_not_of_student', methods=['GET', 'POST'])
@login_required
def get_goal_todos_not_of_student():
 
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))

    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_student_goals'))

    all_goal_todos = Todo.query.filter(Todo.goal_id == std_goal.goal_id)

    student_todos = Todo.query.join(Std_todo).filter(Std_todo.student_id==student.id).filter(Std_todo.goal_id==goal.id).all()

    todos_not_of_student = list(set(all_goal_todos).difference(set(student_todos)))  #todos_not_of_student = all_dst_goal-student_todos

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
   
    return render_template('./documents/edit_std_documents.html', std=std) 
                                                                														  		
@std.route('/edit_student_documents2/<int:selected_student_id>', methods=['GET', 'POST'])
def edit_student_documents2(selected_student_id):
    #########std.id, prf.id("In edit_student_documents2 selected_student_id is :", selected_student_id)
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

    doc.files.append(uploaded_file)

    db.session.add(doc)
    db.session.commit()
        
    
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


##############START studets stds###############	
	
@std.route('/student_dsts', methods=['GET', 'POST'])
@login_required
def student_dsts():
    
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))
    
    tags = Tag.query.order_by(Tag.title).all() 
    default_tag = Tag.query.filter(Tag.selected==True).first()
    if default_tag == None:
        default_tag = Tag.query.filter(Tag.default==True).first()
          
    sub_tags = Sub_tag.query.order_by(Sub_tag.title).all() 
    default_sub_tag = Sub_tag.query.filter(Sub_tag.selected==True).first()
    if default_sub_tag == None:
        default_sub_tag = Sub_tag.query.filter(Sub_tag.default==True).first()
     
    age_ranges = Age_range.query.order_by(Age_range.from_age).all()     
    default_ar = Age_range.query.filter(Age_range.selected==True).first()
    if default_ar == None:
        default_ar = Tag.query.filter(Age_range.default==True).first()
        
    std_gts = General_txt.query.join(Std_general_txt).filter(Std_general_txt.student_id==std.id).filter(Std_general_txt.general_txt_id==General_txt.id).all()
 
    student_dsts = []
    dsts_not_of_student = [] 
    all_dsts = Destination.query.filter(Destination.hide==False).all()  
    for d in all_dsts:
        if d.is_parent_of(default_tag) and d.is_parent_of(default_ar):
            std_dst = Std_general_txt.query.filter(Std_general_txt.student_id==std.id).filter(Std_general_txt.general_txt_id==d.id).first()
            if std_dst != None:
               student_dsts.append(d)
            else:
                dsts_not_of_student.append(d)            
            
            
    student_goals = []    # Get all student's destinations
    all_goals = Goal.query.filter(Goal.hide==False).all()
    for g in std_gts:
        if g in all_goals:
            student_goals.append(g)
    goals_not_of_student = list(set(all_goals).difference(set(student_goals)))  #goals_not_of_student = all_destinations - std_destinations
    
                                  
    student_todos = []    # Get all student's destinations
    all_todos = Todo.query.filter(Todo.hide==False).all()
    for t in std_gts:
        if t in all_todos:
            student_todos.append(t)
    todos_not_of_student = list(set(all_todos).difference(set(student_todos)))  #todos_not_of_student = all_destinations - std_destinations

    author_id = get_author_id()
    todo_obj = Todo("Data Object", "ex", author_id)
    goal_obj = Goal("Data Object", "ex", author_id)
    dst_obj = Destination("Data Object", "ex", author_id)
    '''
    #DEBUG ONLY
    #print("")
    #print("")    
    for d in student_dsts:
        print("D", d.title, d.id)
        for g in student_goals: 
            if d.is_parent_of(g):
                print("   G", g.title, g.id)
            for t in student_todos:
                if g.is_parent_of(t):
                    print("       T", t.title, t.id)
    #print("")
    #print("")  
          
    for d in dsts_not_of_student:
        print("D  NOT_OF_STD ", d.title, d.id)
        for g in goals_not_of_student:
            if d.is_parent_of(g):
                print("   G  NOT_OF_STD", g.title, g.id)
            for t in todos_not_of_student:
                if g.is_parent_of(t):
                    print("       T  NOT_OF_STD", t.title, t.id)
    #print("")
    #print("")
    #DEBUG ONLY
    '''
    
    #print("1111111111111111111111111111111")

    whos = Accupation.query.all()
    default_who = Accupation.query.filter(Status.default==True).first()
    #print("2222222222222222222222222222222")

    statuss = Status.query.all()
    default_status = Status.query.filter(Status.default==True).first()
    #print("33333333333333333333333333")
    
    print("")
    print("")
    print("default_status", default_status)
    print("color", default_status.color)
    print("color_txt", default_status.color_txt)
    print("title", default_status.title)
    print("body", default_status.body)
    print("")
    print("")
  

    std_txts = Std_general_txt.query.filter(Std_general_txt.student_id==std.id).all()

    due_date = date.today()
     
    #print("")
    #print("")

    #print("")
    #print("")
    #print("")
    #print("")
    
    due_date = date.today()
    

    files = Ufile.query.all()   #Reset files selection


    return render_template('./destinations/gts_table/edit_all_gts.html', std=std, due_date=due_date,
                                                        dst_obj=dst_obj, goal_obj=goal_obj, todo_obj=todo_obj,  
                                                        student_dsts=student_dsts, dsts_not_of_student=dsts_not_of_student,
                                                        all_goals=all_goals, student_goals=student_goals, goals_not_of_student=goals_not_of_student, files=files,
                                                        all_todos=all_todos, student_todos=student_todos, todos_not_of_student=todos_not_of_student,
                                                        std_txts=std_txts,
                                                        statuss=statuss, default_status=default_status,
                                                        whos=whos, default_who=default_who,
                                                        tags=tags, default_tag=default_tag,
                                                        sub_tags=sub_tags, default_sub_tag=default_sub_tag,
                                                        age_ranges=age_ranges, default_ar=default_ar)

  
##############START update_std_txt ###############	

@std.route('/update_std_txt', methods=['POST'])
@login_required
def update_std_txt():
    
    #FROM https://stackoverflow.com/questions/43811779/use-many-submit-buttons-in-the-same-form
        
    std_txt = Std_general_txt.query.filter(Std_general_txt.selected==True).first()
       
    if std_txt == None:
        flash("Please select a student and a txt to match  first ")
        return redirect(url_for('students.edit_student_destinations'))		
    
    gt = std_txt.general_txt
     
    gt_sts_name = "sts"+ str(std_txt.general_txt_id)
    
    gt_due_date_name = "due_date" + str(std_txt.general_txt_id)
    
    gt_who_name = "who"+ str(std_txt.general_txt_id)
           
    ##################import pdb;; #pdb.set_trace()

    #print("")
    #print("")
     
    #print("")
    #print("")
    
    ##import pdb; pdb.set_trace()
    
    print("")
    print("")
    print("IN update_std_txt request.form[gt_sts_name]" , request.form[gt_sts_name])
    print("")
    print("")
    
    selected_gt_status = Status.query.filter(Status.title==request.form[gt_sts_name]).first()    
    if selected_gt_status != None:
        std_txt.status_id = selected_gt_status.id     
    sts = set_gt_category(gt.id, 'Status', selected_gt_status.title, 'יש לבחוק סטאטוס לטקסט')  , 
    
    if gt_who_name in request.form:   # Only in case of todo there is a who button
        selected_gt_who = Accupation.query.filter(Accupation.title==request.form[gt_who_name]).first()    
        if selected_gt_who != None:
            std_txt.who_id = selected_gt_who.id     
        who = set_gt_category(gt.id, 'Accupation', selected_gt_who.title, 'יש לבחור תפקיד האחראי על המשימה')  , 
    
    gt_due_date = request.form[gt_due_date_name]                
    if gt_due_date != None:
        std_txt.due_date = gt_due_date
    #gt.due_date = gt_due_date
     
    std_txt.selected = False
        
    db.session.commit()
        
    return  redirect(url_for('students.edit_student_destinations'))


# FROM https://stackoverflow.com/questions/4289331/how-to-extract-numbers-from-a-string-in-python    
import re  # TO EXTRACT NUMBER FROM STRING
@std.route('/update_std_txt2', methods=['GET', 'POST'])
@login_required
def update_std_txt2():

    std = Student.query.filter(Student.selected==True).first()

    if 'selected_ar' in request.form:
        #print("")
        #print("request.form['selected_ar']", request.form['selected_ar'])
        ar = Age_range.query.filter(Age_range.title==request.form['selected_ar']).first()
        if ar != None:
            selected_ar = ar
            selected_ar = age_range_select2(selected_ar.id)
        print("")
        print("")
        print("IN update_std_txt ar = ", ar)
        print("IN update_std_txt selected_ar = ", selected_ar, selected_ar.id)
        print("")        
    
    if 'selected_tag' in request.form:
        print("")
        print("request.form['selected_tag']", request.form['selected_tag'])
        tag = Tag.query.filter(Tag.title==request.form['selected_tag']).first()
        if tag != None:
            selected_tag = tag
            selected_tag = tag_select2(selected_tag.id)
        print("")
        print("IN update_std_txt tag = ", tag)
        print("IN update_std_txt selected_tag = ", selected_tag, selected_tag.id)
        print("")
        print("")
        print("")
        if request.form['txt_type_form_button_name'] == 'std_selected_tag_and_ar':
            return student_dsts()  

    if 'txt_type_form_button_name' in request.form:
        gt_id = int(request.form['txt_type_form_button_name'])
        gt = General_txt.query.filter(General_txt.id == gt_id).first()
        #print("")
        #print("")
        #print("request.form['txt_type_form_button_name'] -- gt: --  ", gt.id. gt.type)
        std_gt = attach_gt_to_std(std.id, gt.id)
        std_gt = std_general_txt_select2(std.id, gt_id)    
       
    if 'dst_tag_or_ar_submit_btn' in request.form:
        gt_id = int(request.form['dst_tag_or_ar_submit_btn'])
        gt = General_txt.query.filter(General_txt.id == gt_id).first()
        #print("")
        #print("")
        #print("request.form['txt_type_form_button_name'] -- gt: --  ", gt.id. gt.type)
        std_gt = attach_gt_to_std(std.id, gt.id)
        std_gt = std_general_txt_select2(std.id, gt_id) 
    
    return update_std_txt()

        
##############END update_std_txt ###############	

########## START attach_gt_to_std #############################

@std.route('/attach_gt_to_std/<int:std_id>/<int:gt_id>', methods=['GET', 'POST'])
def attach_gt_to_std(std_id, gt_id):
        
    ##########import pdb; pdb.set_trace()
    
    std_gt = Std_general_txt.query.filter(Std_general_txt.student_id==std_id).filter(Std_general_txt.general_txt_id==gt_id).first()
    if std_gt == None:
        std_gt = Std_general_txt(std_id, gt_id)
        std_gt.editable = True
        std_gt.due_date = date.today()
        db.session.add(std_gt)
        db.session.commit()
       
        gt = General_txt.query.filter(General_txt.id==gt_id).first()        
        
        sts = Status.query.filter(Status.default==True).first()
        if sts == None:
            flash ("please create a default status first")
            return render_template('gts.edit_gts')            
        std_gt.status_id = sts.id 
     
        who = Accupation.query.filter(Accupation.default==True).first()
        if who == None:
            flash ("please create a default accupation first")
            return render_template('gts.edit_gts')            
        std_gt.acc_id = who.id 

        std = Student.query.filter(Student.id==std_id).first()
        if std_gt not in gt.students:
            gt.students.append(std_gt)
        if std_gt not in std.general_txts:
            std.general_txts.append(std_gt)
        
    db.session.commit()
    return std_gt    

########## START attach_gt_to_std #############################

######### END  student's genearal txt #################################


	
################ START studets gts ##################
	
@std.route('/edit_std_gts', methods=['GET', 'POST'])
@login_required
def edit_std_gts(Gt, Gt_sub, Gt_sub_sub, Gt_sub_sub_sub):   # for example: for student_subjects  ==> Gt = 'Subject' stored  gt.gt_type

    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))
        
    std_gts = []                                             
        
    gt = eval(Gt).query.filter(eval(Gt).selected==True).first()
    if gt != None:   # CASE 1 given GT IS THE ROOT
        std_gts.append(gt)
     
    else:
        ###########################################################
        # Get students gts of Type Gt                              #
        ###########################################################
        for std_gt in std.general_txts:

            #'''
            #################################import pdb;; #pdb.set_trace()
            ###print("")
            #print("")
            ##print("")
            #print("std_gt", std_gt.student, std_gt.general_txt, std_gt.general_txt.title)
            #print("std_gt.general_txt.gt_type", std_gt.general_txt.gt_type)
            #print("GT eval ", Gt, eval(Gt))
            #print("std_gt.general_txt.gt_type == Gt", std_gt.general_txt.gt_type == Gt)
            #print("std_gt.general_txt.gt_type == eval(Gt)", std_gt.general_txt.gt_type == Gt)
            #print("")
            #print("")
            #'''
               
            if std_gt.general_txt.gt_type == Gt:
                std_gts.append(std_gt.general_txt)
       
   #''' 
    #print("")
    #print("")   
    #print("std_gts", std_gts)
    #print("")
    #print("")
    #'''
    all_gts  = eval(Gt).query.all()                                                  
    gts_not_of_student = list(set(all_gts).difference(set(std_gts)))  #main_gts_not_of_student = all_main_gts - std_gts
    
    ###print("std_gts", std_gts)
    ###print("")
    
    # Get gt's categories
    gt_categories = []  
    for std_gt in std_gts:    
        for x in get_categories_of(std_gt):
            if x not in gt_categories:
                gt_categories.append(x)

    #####################################import pdb;; #pdb.set_trace()
    
    ##################################################################                                
    ######### Level2 -- Gt's children of Type in Categories ##########
    ##################################################################     
    gt_subs = []
    gt_subs_not_of_std=[]
    for gt in std_gts: 
        gt_subs.extend(get_gt_all_categories_children(gt))     
        gt_subs_not_of_std = gt_subs_not_of_std+get_gt_all_categories_children_not_of_std(std, gt)  #main_gts_not_of_student = all_main_gts - std_gts
    
    #'''
    #NOT OF DEBUG 
    #print("gt_subs : ", gt_subs)
    #print("")
    #print("gt_subs_not_of_std : ",gt_subs_not_of_std)    
    #NOT OF DEBUG
    #'''       

    ##################################################################                                
    ######### Level3 -- Gt's children of Type in Categories ##########
    ##################################################################        
    gt_sub_subs = []
    gt_sub_subs_not_of_std = []
    if Gt_sub_sub != 'None':
        for gt in gt_subs: 
            gt_sub_subs.extend(get_gt_all_categories_children(gt))            
            gt_subs_not_of_std = gt_subs_not_of_std+get_gt_all_categories_children_not_of_std(std, gt)  #main_gts_not_of_student = all_main_gts - std_gts
   
    ##################################################################                                
    ######### Level4 -- Gt's children of Type in Categories ##########
    ##################################################################        
    gt_sub_sub_subs = []
    gt_sub_sub_subs_not_of_std = []
    if Gt_sub_sub_sub != 'None':
        for gt in gt_sub_subs: 
            gt_sub_sub_subs.extend(get_gt_all_categories_children(gt))  
            gt_sub_sub_subs_not_of_std = gt_sub_sub_subs_not_of_std+get_gt_all_categories_children_not_of_std(std, gt)  #main_gts_not_of_student = all_main_gts - std_gts
    
    #'''
    #print("")
    #print("")
    #print("gt_sub_subs", gt_sub_sub_subs)
    #print("")
    #print("gt_sub_sub_subs_not_of_std", gt_sub_sub_subs_not_of_std)
    #print("")
    #print("")
    #'''
    
    whos = Accupation.query.all()
    default_who = Accupation.query.filter(Accupation.default==True).first()

    statuss = Status.query.all()
    default_status = Status.query.filter(Status.default==True).first()
        
    tags = Tag.query.order_by(Tag.title).all() 
    default_tag = Tag.query.filter(Tag.selected==True).first()
    if default_tag == None:
        default_tag = Tag.query.filter(Tag.default==True).first()
     
    age_ranges = Age_range.query.order_by(Age_range.from_age).all()     
    default_ar = Age_range.query.filter(Age_range.selected==True).first()
    if default_ar == None:
        default_ar = Age_range.query.filter(Age_range.default==True).first()
    
    std_txts = Std_general_txt.query.filter(Std_general_txt.student_id==std.id).all()

    due_date = date.today()
      
    #print("")
    #print("")
    #print("IN edit_std_gts, BEFORE calling edit_all_main_gts.html --- gt_subs: ", gt_subs)
    #print("")
    #print("")
    return render_template('./gts/table_gts/edit_all_main_gts.html', std=std,  
                                                        std_gts=std_gts, gts_not_of_student=gts_not_of_student, gt_categories=gt_categories,
                                                        gt_subs=gt_subs, gt_subs_not_of_std=gt_subs_not_of_std,
                                                        gt_sub_subs=gt_sub_subs, gt_sub_subs_not_of_std=gt_sub_subs_not_of_std,
                                                        statuss=statuss, default_status=default_status,
                                                        whos=whos, default_who=default_who,
                                                        tags=tags, age_ranges=age_ranges,
                                                        due_date=due_date)
                                                
														  		
@std.route('/edit_std_gts2/<int:selected_student_id>/<int:selected_gt_id>', methods=['GET', 'POST'])
@login_required
def edit_std_gts2(selected_student_id, selected_gt_id, Gt, Gt_sub, Gt_sub_sub, Gt_sub_sub_sub):

    std = student_select2(selected_student_id)
    gt = specific_gt_type_select2(selected_gt_id, Gt)
    return edit_std_gts(Gt, Gt_sub, Gt_sub_sub, Gt_sub_sub_sub)


 														  		
@std.route('/get_std_gt/<int:std_id>', methods=['GET', 'POST'])
@login_required
def get_std_gt(std_id, Gt):
    
    ###print(" IN get_std_gt   std_id Gt ", std_id, Gt)
    ############################import pdb;; #pdb.set_trace()
    
    all_std_gts = Std_general_txt.query.filter(Std_general_txt.student_id==std_id).all()
    all_type_gts = eval(Gt).query.all()
       
    for type_gt in all_type_gts:
        for std_gt in all_std_gts:
            if std_gt.general_txt in all_type_gts:
                gt = std_gt.general_txt  

    if gt != None:
        std_gt = std_general_txt_select2(std_id, gt.id)

    return gt
    
################ END studets gts ##################


################ START studets PROFILE ##################

@std.route('/edit_profile2_by_tag', methods=['GET', 'POST'])
@login_required
def edit_profile2_by_tag():
    return redirect(url_for('students.std_edit_profile2', selected_student_id=get_dummy_student().id,
                                                          dsply_direction=1))

   	   
@std.route('/reset_and_get_profile', methods=['GET', 'POST'])
def reset_and_get_profile(selected_student_id):

    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("IN get_std_prf_parts Please select a student first ")
        return redirect(url_for('students.edit_students'))

    prf = Profile.query.filter(Profile.body==str(std.id)).first()
    if prf == None:
        flash ("Setting a new Profile for Student: {0} {1} ID: {2}".format(std.first_name, std.last_name, std.id))
        prf = Profile(std.first_name+'s Profile', str(std.id), get_author_id())	
        db.session.add(prf)
        db.session.commit()
        std_gt = attach_gt_to_std(std.id, prf.id) 

    prf = profile_select2(prf.id)

    return prf



@std.route('/std_edit_profile/<int:dsply_direction>', methods=['GET', 'POST'])
@login_required
def std_edit_profile(dsply_direction):

    print("")
    print("")
    print("IN get_profile_data")
    print("")
    
    #DEBUG - ARESE!

    #DEBUG - ARESE!
    
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))
        
    profile = reset_and_get_profile(std.id)
    
    
    tags = Tag.query.order_by(Tag.title).all()
    default_tag = Tag.query.filter(Tag.selected==True).first()
    if default_tag == None:
        for t in tags:
            if t.default==True:
                default_tag = t
 
 
    sub_tags = Sub_tag.query.all()
    std_sub_tags = []
    for st in sub_tags:
        if default_tag.is_parent_of(st):
            std_sub_tags.append(st)
            

    default_sub_tag = Sub_tag.query.filter(Sub_tag.selected==True).first()
    if default_sub_tag == None:
        for st in std_sub_tags:
            if st.default==True:
                default_sub_tag = st
                break

    all_tag = Tag.query.filter(Tag.body=='all').first()
    all_sub_tag = Sub_tag.query.filter(Sub_tag.body=='all').first()
    all_sub_tags = all_sub_tag
    
    print("")
    print("")
    print("IN END OF std_edit_profile DEFAULT-TAG: {0}  DEFAULT-SUB-TAG: {1} ".format( default_tag.id, default_sub_tag.id))
    print("")
    
    
    form = Gt_form()
    
    form.tag.choices = [(tag.id, tag.title) for tag in tags]
    form.tag.default = default_tag.id
    form.process()
    
    form.sub_tag.choices = [(sub_tag.id, sub_tag.title) for sub_tag in std_sub_tags]
    form.sub_tag.default = default_sub_tag.id
    form.process()
    
    prf_subjects=[]
    subjects_not_of_prf=[]
    all_subjects = Subject.query.all()
    for s in all_subjects:
        if profile.is_parent_of(s):
            prf_subjects.append(s)
        else:
            if s.hide == False: 
                subjects_not_of_prf.append(s)
            
    prf_weaknesses=[]
    weaknesses_not_of_prf=[]
    all_weaknesses = Weakness.query.all()
    for s in all_weaknesses:
        if profile.is_parent_of(s):
            prf_weaknesses.append(s)
        else:
            if s.hide == False:
                weaknesses_not_of_prf.append(s)
            
    prf_strengths=[]
    strengths_not_of_prf=[]
    all_strengths = Strength.query.all()
    for s in all_strengths:
        if profile.is_parent_of(s):
            prf_strengths.append(s)
        else:
            if s.hide == False:
                strengths_not_of_prf.append(s)
            
            
    user = User.query.get_or_404(current_user._get_current_object().id)
    author_id = user.id
    
    sbj = Subject.query.filter(Subject.title=='Subject_data').first()
    if sbj==None:
        sbj = Subject('Subject_data', 'Subject_data', author_id)
    sbj.odd_color = '#e6f2ff'   
    sbj.even_color = '#cce5ff'
       
    strn = Strength.query.filter(Strength.title=='Subject_data').first()
    if strn==None:
        strn = Strength('Strength_data', 'Strength_data', author_id)
    
    print("")
    print("")
    print("std_edit_profile")
    print("STRN ODD: ", strn.odd_color)
    print("STRN EVEN: ", strn.even_color)
    print("")
    print("")
    
    weak = Weakness.query.filter(Weakness.title=='Subject_data').first()
    if weak==None:
        weak = Weakness('Weakness', 'Weakness', author_id)
    #weak.odd_color = '#ffe6e6'
    #weak.even_color = '#ffb3b3'
    
    gray = Gray.query.filter(Gray.title=='gray data').first()
    if gray==None:
        gray = Gray('Gray', 'Gray', author_id)

    print("IN END OF std_edit_profile Calling std_edit_profile.html")
    print("")
    print("")
    
    if dsply_direction == 1:
        return render_template('./profile/std_edit_profile.html', 
                                std=std,
                                profile=profile, 
                                sbj=sbj, strn=strn, weak=weak, gray=gray,
                                tags=tags, default_tag=default_tag, all_tag=all_tag,
                                sub_tags=sub_tags, default_sub_tag=default_sub_tag, all_sub_tags=all_sub_tags, all_sub_tag=all_sub_tag,
                                prf_subjects=prf_subjects, subjects_not_of_prf=subjects_not_of_prf,
                                prf_weaknesses=prf_weaknesses, weaknesses_not_of_prf=weaknesses_not_of_prf,
                                prf_strengths=prf_strengths, strengths_not_of_prf=strengths_not_of_prf )

    else:
        return render_template('./profile/vertical_dsply/profile_verical_dsply.html', 
                                std=std, form=form, 
                                profile=profile, 
                                sbj=sbj, strn=strn, weak=weak, gray=gray,
                                tags=tags, default_tag=default_tag, all_tag=all_tag,
                                sub_tags=sub_tags, default_sub_tag=default_sub_tag, all_sub_tags=all_sub_tags, all_sub_tag=all_sub_tag,
                                prf_subjects=prf_subjects, subjects_not_of_prf=subjects_not_of_prf,
                                prf_weaknesses=prf_weaknesses, weaknesses_not_of_prf=weaknesses_not_of_prf,
                                prf_strengths=prf_strengths, strengths_not_of_prf=strengths_not_of_prf )

				
                
@std.route('/std_edit_profile2/<int:selected_student_id>/<int:dsply_direction>', methods=['GET', 'POST'])
@login_required
def std_edit_profile2(selected_student_id, dsply_direction):

    std = student_select2(selected_student_id)
    prf = reset_and_get_profile(std.id) 
   
    return redirect(url_for('students.std_edit_profile', dsply_direction=dsply_direction))

import sys
#FROM  https://stackoverflow.com/questions/45131503/unable-to-receive-data-from-ajax-call-flask
@std.route('/get_sub_tag_profile', methods=['GET', 'POST'])
def get_sub_tag_profile():
    
    if 'show_std_profile' in request.form:   # GET AND SAVE SUB TAGS
        print("")
        print(request.form['show_std_profile'])
        
    if 'get_sub_tag_profile' in request.form:   # GET AND SAVE SUB TAGS
        print("")
        print("get_sub_tag_profile:")
        print(request.form['get_sub_tag_profile'])
        print("")
        
    if 'tag' in request.form:   # GET AND SAVE TAGS
        form_tag = Tag.query.filter_by(id=request.form['tag']).first()
        if form_tag != None:
            selected_tag = tag_select2(form_tag.id)

        print("")
        print("")
        print("IN --- get_sub_tag_profile --- form_tag: ", request.form['tag'], form_tag)
        
    if 'sub_tag' in request.form:   # GET AND SAVE TAGS
        form_sub_tag = Sub_tag.query.filter_by(id=request.form['sub_tag']).first()
        print("form_sub_tag: ", request.form['sub_tag'], form_sub_tag)
        print("IN --- get_sub_tag_profile --- 'tag' in request.form: ", 'tag' in request.form)
        print("")
        print("")
        #sub_tag_id = re.sub(r"\D", "", form_sub_tag)
        if form_sub_tag == None:
            flash("נא ךבחור נושא וקטגוריה")
            return redirect(url_for('gts.edit_gts'))
  
        sub_tag = Sub_tag.query.filter(Sub_tag.id==form_sub_tag.id).first()

        if sub_tag != None:
            selected_sub_tag = sub_tag_select2(sub_tag.id)
        else:
            selected_sub_tag = get_default_child(selected_tag, 'Sub_tag')
            if selected_sub_tag == None:
                flash("חסר תת קטגוריה לנושר {0} בבקשה תצור אחד.".format(selected_tag.title))
                return redirect(url_for('gts.edit_gts'))
    
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("IN get_sub_tag_profile Please select a student first ")
        return redirect(url_for('students.edit_students'))
        
    prf = reset_and_get_profile(std.id)

    prf.set_parent(selected_tag)
    prf.set_parent(selected_sub_tag)
    db.session.commit()
    
    print("")
    print("")
    st = Sub_tag.query.filter(Sub_tag.selected==True).first()
    t = Tag.query.filter(Tag.selected==True).first()
    print("IN END OF sub_tag_profile selected_tag={0} selected_sub_tag = {1} ".format( t.id, st.id))
    print("")
    print("")
    sys.stdout.flush()

    return std_edit_profile(0)
   
        
@std.route('/tag_sub_tag_to_profile_add', methods=['GET', 'POST'])
def tag_sub_tag_to_profile_add():
            
    print("")
    print("")
    print("IN tag_sub_tag_to_profile_add ")

    tag_id =  request.form['tag_id']
    sub_tag_id = request.form['sub_tag_id']

    
    #print("tag_id: ", tag_id)
    print("sub_tag_id: ", sub_tag_id)
      
    tag = tag_select2(tag_id)
    sub_tag = sub_tag_select2(sub_tag_id)
    
    print("")
    print("")
    print("IN tag_sub_tag_to_profile_add AFTER SELECT2: ")
    print("tag_id: ", tag.id)
    print("sub_tag_id: ", sub_tag.id)
    
    profile = Profile.query.filter(Profile.selected==True).first()
    profile.set_parent(tag)
    profile.set_parent(sub_tag)
    
    newSubj = Subject('New', 'New', get_author_id())
    
    profile.set_parent(newSubj)
    tag.set_parent(newSubj)
    sub_tag.set_parent(newSubj)
    
    newSubj.set_parent(tag)
    newSubj.set_parent(sub_tag)
    
    db.session.commit()
    
    print("")
    print("")
    print("IN END OF tag_sub_tag_to_profile_add , calling std_edit_profile")
    print("")
    print("")
    
    return std_edit_profile(1)
  
        
#FROM https://youtu.be/I2dJuNwlIH0?t=583
@std.route('/sub_tag/<tag_id>', methods=['GET', 'POST'])
def sub_tag(tag_id):
            
    print("")
    print("")
    print("IN sub_tag ")
    print("tag_id: ", tag_id)
      
    tag = Tag.query.filter(Tag.id==tag_id).first()
    sub_tags_array =[]
    all_sub_tags = Sub_tag.query.all()
    
    print("")
    print("")
    
    for st in all_sub_tags:
        sub_tag_obj = {}   #JSON STYLE
        if tag.is_parent_of(st):
            print("IN SUB_TAG RETURNING TO JS FETCH CALL")
            print("SUB: ", st.id, st.title)
            print("")
            sub_tag_obj['id'] = st.id
            sub_tag_obj['title'] = st.title
            sub_tags_array.append(sub_tag_obj)
            
    print("")
    print("")
    print("IN sub_tag ")
    print("sub_tags_array: ", sub_tags_array)
        
    return jsonify({'sub_tags': sub_tags_array})
  

#### POST CASE ####                                                                                     
@std.route('/std_part_to_prf_add/<int:dsply_direction>', methods=['GET', 'POST'])
def std_part_to_prf_add(new_gt_type, new_gt_id, new_gt_title, new_gt_body, tag_id, sub_tag_id, dsply_direction):

    print("")
    print("")
    
    print(" IN std_part_to_prf_add")

    if tag_id == 0:
        tag = Tag.query.filter(Tag.selected==True).first()
        if tag == None:
            flash ("יש לבחור נושא")
            return std_edit_profile(0)
        tag_id = tag.id
            
       
    if sub_tag_id == 0:
        sub_tag = Sub_tag.query.filter(Sub_tag.selected==True).first()
        if sub_tag == None:
            flash ("יש לבחור תת נושא")
            return std_edit_profile(0)
        sub_tag_id = sub_tag_id = sub_tag.id
            
            
    print("TAG-ID ", tag_id)
    print("SUB-ID ", sub_tag_id)
    print("")
    print("")
    tag = Tag.query.filter(Tag.id==tag_id).first()
    
    sub_tag = Sub_tag.query.filter(Sub_tag.id==sub_tag_id).first()
    
    print("")
    print("")
    print("IN std_part_to_prf_add")
    print("TAG: ", tag, tag.id)
    print("SUB-TAG: ", sub_tag, sub_tag.id) 
    print("")
    print("")

    profile = Profile.query.filter(Profile.selected=='True').first()
    if profile == None:
        flash("Please select a profile to add a part to ")
        return redirect(url_for('students.std_edit_profile', dsply_direction=dsply_direction) ) 
        
    ### POST Case
    ### FROM https://stackoverflow.com/questions/28209131/wtforms-post-with-selectfield-not-working
    ##print ("form.validate_on_submit", form.validate_on_submit)
    
    print("In std_part_to_prf_add profile is :", profile, profile.id)
    print("")    
    print("")    
    print("In std_part_to_prf_add new_gt_title is :", new_gt_title)
    print("")    
    print("In std_part_to_prf_add new_gt_id is :", new_gt_id)
    print("")
    print("In std_part_to_prf_add new_gt_body is :", new_gt_body)
    print("")
    print("In std_part_to_prf_add gt_type is :", new_gt_type)
    print("")
    print("")
    print(" *** In std_part_to_prf_add TAG is :", tag, tag.id)
    print("")
    print(" *** In std_part_to_prf_add SUB_TAG is :", sub_tag, sub_tag.id)
    print("")
    
    author_id = current_user._get_current_object().id 
    
    new_gt = eval(new_gt_type).query.filter(eval(new_gt_type).id==new_gt_id).first()
    if new_gt == None:    
        new_gt = eval(new_gt_type).query.filter(eval(new_gt_type).title==new_gt_title). \
                                         filter(eval(new_gt_type).body==new_gt_body).first()
        if new_gt == None:
            new_gt = eval(new_gt_type)(new_gt_title, new_gt_body, author_id)
            db.session.add(new_gt)
            db.session.commit()
        
    #print("new_gt.id  ", new_gt.id)
    
    #new_gt = general_txt_select2(new_gt.id)
    
    new_gt.title = new_gt_title
    new_gt.body =  new_gt_body
    
    db.session.add(new_gt)
    db.session.commit()
    
    #new_gt = general_txt_select2(new_gt.id)
    all_tag =  Tag.query.filter(Tag.body=='all').first()
    
    new_gt.set_parent(tag)
    new_gt.set_parent(all_tag)

    tag.set_parent(new_gt)
    all_tag.set_parent(new_gt)


    
    all_sub_tag =  Sub_tag.query.filter(Sub_tag.body=='all').first()
    
    #import pdb; pdb.set_trace()
    
    new_gt.set_parent(sub_tag)
    new_gt.set_parent(all_sub_tag)

    sub_tag.set_parent(new_gt)
    all_sub_tag.set_parent(new_gt)

    
    scrt = Scrt.query.filter(Scrt.body=='Private').first()
    if scrt == None:
        flash ("No such Secirity option: Private")
        redirect(url_for('gts.edit_gts'))
        
    print("")
    print("")
    print("IN std_part_to_prf_add")
    print("new_gt", new_gt)
    print("new_gt", new_gt.id, new_gt.title)
    print("scrt", scrt)
    print("scrt", scrt.id, scrt.title)
    print("")
    print("")

    new_gt.set_parent(scrt)
    scrt.set_parent(new_gt)
       
    db.session.commit()

    std = get_dummy_student()   # Match new gt to Humpty Dumpty
    std_gt = attach_gt_to_std(std.id, new_gt.id) 
    
    ####################################import pdb;; pdb.set_trace()
    profile.set_parent(new_gt)
    profile.set_parent(tag)
    profile.set_parent(sub_tag)
    
    humpty_prf = Profile.query.filter(Profile.body==str(get_dummy_student().id)).first()
    humpty_prf.set_parent(new_gt)
    humpty_prf.set_parent(tag)
    humpty_prf.set_parent(sub_tag)
    
    print("")
    print("")
    print("IN std_part_to_prf_add")
    print("Hynpty prf", humpty_prf.id, humpty_prf.title, humpty_prf.body)
    print("Add Part: ", new_gt.id, new_gt.title, new_gt.body)
    print("")
   
    #selected_sub_tag = Sub_tag.query.filter(Sub_tag.selected==True).first()
    ##print(" In END OF gt_to_profile_add SUB_GT =: " ,selected_sub_tag, selected_sub_tag.id)
    ##print(" In END OF gt_to_profile_add NEW_GT =: " ,new_gt.id,  new_gt.gt_type)
    
    new_gt.selected = False
    db.session.commit()
    
    return std_edit_profile(dsply_direction)
          

@std.route('/std_part_to_prf_add2/<int:tag_id>/<int:sub_tag_id>/<int:dsply_direction>', methods=['GET', 'POST'])
def std_part_to_prf_add2(tag_id, sub_tag_id, dsply_direction):

    print("")
    print("")
    
    print(" IN std_part_to_prf_ADD2")
    
    if tag_id == 0:
        tag = Tag.query.filter(Tag.selected==True).first()
        if tag == None:
            flash ("יש לבחור נושא")
            return std_edit_profile(0)
        tag_id = tag.id
            
       
    if sub_tag_id == 0:
        sub_tag = Sub_tag.query.filter(Sub_tag.selected==True).first()
        if sub_tag == None:
            flash ("יש לבחור תת נושא")
            return std_edit_profile(0)
        sub_tag_id = sub_tag_id = sub_tag.id
            
                
            
    print("TAG-ID ", tag_id)
    print("SUB-ID ", sub_tag_id)
    print("")
    print("")
    
    
    
    #################import pdb; pdb.set_trace()
    
    #print("request.form['gt_title'] ",   request.form['gt_title'])
    #print("request.form['gt_body'] ",    request.form['gt_body'])
    #print("request.form['class_name'] ", request.form['class_name'])

    new_gt_title =  request.form['gt_title']
    new_gt_body =  request.form['gt_body']
    new_gt_type =  request.form['class_name']
        
    return std_part_to_prf_add(new_gt_type, 0, new_gt_title, new_gt_body, tag_id, sub_tag_id, dsply_direction) 



    
@std.route('/std_prf_part_update', methods=['GET', 'POST'])
def std_prf_part_update(gt_type, gt_title, gt_body):
    
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please IN std_prf_part_update select a student first ")
        return redirect(url_for('students.std_edit_students'))
     
    prf = reset_and_get_profile(std.id)
    if prf == None:
        flash("IN std_prf_part_update There is no Profile for Student {0} ".format(std.id))
        return redirect(url_for('students.std_edit_profile', dsply_direction=1))		

    selected_tag = Tag.query.filter(Tag.selected==True).first()
    if selected_tag == None:
        for t in Tag.query.all():
            if t.default==True:
                selected_tag = t 
        
    selected_sub_tag = Sub_tag.query.filter(Sub_tag.selected==True).first()
    if selected_sub_tag == None:
        for st in Sub_tag.query.all():
            if (st.default==True) and (t.is_parent_of(st)):
                selected_sub_tag = t 
        
    updated_gt = General_txt.query.filter(General_txt.selected==True).filter(General_txt.type==gt_type).first()    
    if updated_gt == None:
        flash("IN std_prf_part_update Please part select a profile part to update")
        return redirect(url_for('students.std_edit_profile', dsply_direction=1) )
   

    print("")
    print("")
    print("IN END OF std_prf_part_update updated_gt: ")
    print("IN std_prf_part_update PRF: ", prf, prf.id)
    print("IN std_prf_part_update SELECT TAG: ", selected_tag, selected_tag.id)
    print("IN std_prf_part_update SELECTED SUB TAG: ", selected_sub_tag)
    print("")
    print("IN std_prf_part_update updated_GT-ID: ", updated_gt.id)
    print("IN std_prf_part_update updated_GT_TYPE: ",  updated_gt.type)
    print("IN std_prf_part_update updated_gt: ",  updated_gt.class_name)

        
    print("")
    #print("")
    #print("")
    #print("")
    
    
    new_prf_part = eval(updated_gt.class_name)(gt_title, gt_body, get_author_id())
    db.session.add(new_prf_part)
    db.session.commit()
    
    print("IN std_prf_part_update updated_GT TITLE: ", updated_gt.title)
    print("IN std_prf_part_update updated_GT BODY: ",  updated_gt.body)
    print("")  
    
    std_gt = attach_gt_to_std(std.id, new_prf_part.id)
    #db.session.add(std_gt)   already done in attach function
    db.session.commit()
    
    
    prf.unset_parent(updated_gt)
    prf.set_parent(new_prf_part)
    humpty_prf = Profile.query.filter(Profile.body==str(get_dummy_student().id)).first()
    humpty_prf.set_parent(new_prf_part)
        
    #print("")
    print("IN END OF std_prf_part_update TAG SUB_TAG ", selected_tag, selected_sub_tag)
    print("")
    print("")
    #print("")
    
    new_prf_part.set_parent(selected_tag)
    new_prf_part.set_parent(selected_sub_tag)
    #attach_gt_to_std(get_dummy_student().id, new_prf_part.id)
    
    #############import pdb; pdb.set_trace()
   
    #print("")
    ##print("IN END OF std_prf_part_update prf, std_gt=", prf, std_gt)
    #print("")
    #print("")
    #print("")
    
    updated_gt.selected = False
    
    #########import pdb; pdb.set_trace()
    
    db.session.commit()
    return std_edit_profile(1)
    
#### POST CASE ####                                                                                     
@std.route('/std_prf_part_update2/<int:selected_gt_id>', methods=['GET', 'POST'])
def std_prf_part_update2(selected_gt_id):
   
    print("")
    print("")
    print("")
    print("")   
    print(" IN std_profile_gt_update2: selected_gt_id", selected_gt_id)

   
    gt = gt_type_select2(selected_gt_id)
   
    gt_title = request.form['gt_title']
    gt_body = request.form['gt_body']
    gt_type = gt.type
    
    print("Calling std_prf_part_update with  gt_type, gt_title, gt_body", gt_type, gt_title, gt_body)
    print("")
    #print("")
    #print("")
    #print("")
    #print("")
    return std_prf_part_update(gt_type, gt_title, gt_body)	
           

@std.route('/attach_prf_part_to_std2/<int:selected_gt_id>/<int:tag_id>/<int:sub_tag_id>/<int:dsply_direction>', methods=['GET', 'POST'])
def attach_prf_part_to_std2(selected_gt_id, tag_id, sub_tag_id, dsply_direction):

    print("")
    print("")
    print(" IN ATTACH_prf_part_to_std2")
    print(" selected_gt_id, tag_id, sub_tag_id", selected_gt_id, tag_id, sub_tag_id)
    print("")
    print("")
    
    gt = gt_type_select2(selected_gt_id)
    
    return std_part_to_prf_add(gt.class_name, gt.id, gt.title, gt.body, tag_id, sub_tag_id, dsply_direction) 


@std.route('/std_part_from_prf_delete', methods=['GET', 'POST'])
def std_part_from_prf_delete():
    
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please IN std_prf_part_update select a student first ")
        return redirect(url_for('students.std_edit_students'))
     
    prf = reset_and_get_profile(std.id)
    if prf == None:
        flash("IN std_prf_part_update There is no Profile for Student {0} ".format(std.id))
        return redirect(url_for('students.std_edit_profile', dsply_direction=1))		

    prf.unset_parent(gt)
    if std.id == get_dummy_student().id:
        gt.hide = True
    db.session.commit()  

    return redirect(url_for('students.std_edit_profile', dsply_direction=1)) 


@std.route('/std_part_from_prf_delete2/<int:selected_gt_id>/<int:dsply_direction>', methods=['GET', 'POST'])
#Here author is user_id
def std_part_from_prf_delete2(selected_gt_id, dsply_direction):
   
    print(" IN gt_from_profile_DELETE2:  selected_gt_id", selected_gt_id)
    
    gt = General_txt.query.filter(General_txt.id==selected_gt_id).first()
    
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please IN std_prf_part_update select a student first ")
        return redirect(url_for('students.std_edit_students'))
     
    prf = reset_and_get_profile(std.id)
    if prf == None:
        flash("IN std_prf_part_update There is no Profile for Student {0} ".format(std.id))
        return redirect(url_for('students.std_edit_profile', dsply_direction=dsply_direction))		

    prf.unset_parent(gt)
    if std.id == get_dummy_student().id:
        gt.hide = True
    db.session.commit()      
    return redirect(url_for('students.std_edit_profile', dsply_direction=dsply_direction)) 	

  
################ END studets PROFILE ##################
	 
     
@std.route('/get_gt_categories_children', methods=['GET', 'POST'])
@login_required
def get_gt_all_categories_children(gt):  

    ###################################import pdb;; #pdb.set_trace()
     
    # Get gt's categories
    gt_categories = []    
    for x in get_categories_of(gt):
        if x not in gt_categories:
            gt_categories.append(x)

    ######print("IN get_gt_categories_children -- gt_categories --: ", gt_categories)
    ######print("")
       
    gt_all_categories_subs = []
    for ctg in gt_categories:
     
       gt_all_categories_subs.extend(get_gt_children_of_category(gt, ctg)) 
   
    ##print("")
    ##print("")
    ##print("IN get_gt_categories_children -- gt_all_categories_subs --: ", gt_all_categories_subs)
    ##print("")
    
    return gt_all_categories_subs
 
 
@std.route('/get_gt_children_of_category', methods=['GET', 'POST'])
@login_required
def get_gt_children_of_category(gt, Ctg):

    ################################import pdb;; #pdb.set_trace()
    ##print("gt", gt)
    ##print("")
    ##print("gt.id", gt.id)
    ##print("")
    ##print("gt.gt_type", gt.gt_type)
    ##print("")
    ##print("gt.type", gt.type)
    ##print("")
    ##print("Ctg", Ctg)
    ##print("")
    ##print("Ctg.gt_type", Ctg.gt_type)
    ##print("")
     
    ######################import pdb;; #pdb.set_trace()
    gt_ctg_children = []
    #all_ctg_gts = Ctg.query.all()   # Example: Get all Subjects/Weaknesses/Strengths
    all_ctg_gts = General_txt.query.filter(General_txt.type== Ctg.gt_type.lower()).all()  # Example: Get all Subjects/Weaknesses/Strengths
    for c in gt.children:
        if c in all_ctg_gts:
            gt_ctg_children.append(c) 

    ##print(" IN f", gt_ctg_children)
    ##print("")
    ##print("")
    
    return gt_ctg_children

	 
     
@std.route('/get_gt_all_categories_children_not_of_std', methods=['GET', 'POST'])
@login_required
def get_gt_all_categories_children_not_of_std(std, gt):  

    #########################import pdb;; #pdb.set_trace()
    
    # Get gt's categories
    gt_categories = []    
    for x in get_categories_of(gt):
        if x not in gt_categories:
            gt_categories.append(x)

    ###print("IN get_gt_all_categories_children_not_of_std -- gt_categories --: ", gt_categories)
    ###print("")
    ##################################import pdb;; #pdb.set_trace()
    
    gt_all_categories_subs_not_of_std = []
    for ctg in gt_categories:
        gt_all_categories_subs_not_of_std.extend(get_gt_children_of_category_not_of_std(std, ctg.class_name)) 
    
    ##print("IN get_gt_all_categories_children_not_of_std -- gt_all_categories_subs_not_of_std --: ", gt_all_categories_subs_not_of_std)
    ##print("")
    
    return gt_all_categories_subs_not_of_std
 
 
@std.route('/get_gt_children_of_category_not_of_std', methods=['GET', 'POST'])
@login_required
def get_gt_children_of_category_not_of_std(std, Ctg):
        
    ########################import pdb;; #pdb.set_trace()
    
    gt_ctg_children_not_of_std = []
    
    all_ctg_gts =   General_txt.query.filter(General_txt.type==Ctg.lower()).all()
    
    #std_gts = Std_general_txt.query.with_entities(Std_general_txt.general_txt).filter(Std_general_txt.student_id==std.id).all()
    
    std_gts = General_txt.query.join(Std_general_txt).filter(Std_general_txt.student_id==std.id).all()
   
    ###print("IN LINE 2148:",all_ctg_gts)
    ###print("")
   
    ###print("IN IN LINE 2151 std std_gts:",std_gts)
    ###print("")
   
    gt_ctg_children_not_of_std = list(set(all_ctg_gts).difference(set(std_gts)))  #x_not_of_student = all_x - std_x
    
    '''
    for ctg_gt in all_ctg_gts:
        for std_gt in std_gts:        
            if ctg_gt not in std_gts:
                #####print("ctg_gt: ", ctg_gt)
                #####print("")
                gt_ctg_children_not_of_std.append(ctg_gt) 
    '''
    #####print(" IN get_gt_children_of_category_not_of_std", gt_ctg_children_not_of_std)
    
    return gt_ctg_children_not_of_std

#***********************************************

    ############## START UPDATE STD GT ################

@std.route('/update_std_gt', methods=['POST'])
@login_required
def update_std_gt():
     
    ####print(" IN update_std_gt:")
    ####print("")
    
    #####################################import pdb;; #pdb.set_trace()
        
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))
    
   
    std_prf = get_std_gt(std.id, 'Profile')
    ####print(" IN update_std_gt std profile: ", std_prf)
    
    gt = General_txt.query.filter(General_txt.selected == True).filter(General_txt.type!='profile').first()           
    
    std_gt = Std_general_txt.query.filter(Std_general_txt.student_id==std.id).filter(Std_general_txt.general_txt_id==gt.id).first()
    if std_gt == None:    
        ####print(" attaching std.id to gt.id", std.id, gt.id)
        ####print("")
        std_gt = attach_gt_to_std(std.id, gt.id)
     
    #####################################import pdb;; #pdb.set_trace()
    ####print(" IN update_std_gt setting gt to be a child of orf profile", gt, std_prf)
    ####print("")
    ####print("")
    
    std_prf.set_parent(gt)

    gt.selected = False
        
    db.session.commit() 

    return  redirect(url_for('students.std_edit_profile2', selected_student_id=std.id )) 


@std.route('/update_std_gt2', methods=['GET', 'POST'])
@login_required
def update_std_gt2():
    
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))
   
    gt_id = int(request.form['save_gt'])    
 
    #print("")
    #print("")
    #print("IN update_std_gt2 -- gt_id:", gt_id)
    #print("")
        
    current_prf = Profile.query.filter(Profile.selected==True).first()
        
    ####print("IN update_std_gt2  current_prf", current_prf)
    gt = General_txt.query.filter(General_txt.id==gt_id).first()
    gt = specific_gt_type_select2(gt_id, gt.gt_type)
    
    prf = profile_select2(current_prf.id)
         
    gt_title_name = "title"+ str(gt.id)    
    gt_body_name =  "body" + str(gt.id)
       
    gt.title = request.form[gt_title_name]
    gt.body =  request.form[gt_body_name]
    
    std_gt = attach_gt_to_std(std.id, gt.id)
    prf.set_parent(gt)
    
    db.session.commit()
                   
    return update_std_gt()
    
    ############## START UPDATE STD GT ################
    
