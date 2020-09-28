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
from app.select.select import std_general_txt_select2, general_txt_select2, specific_gt_type_select2
from app.select.select import destination_select2, goal_select2, todo_select2, std_goal_select2, document_select2
from app.select.select import profile_select2, strength_select2, subject_select2, weakness_select2

from app.gts.gts import get_categories_of

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
from app.select.select import teacher_select2, student_select2, todo_select2
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

    #######import pdb; pdb.set_trace()
    
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
        
    print("IN show_student_tree student_dsts ", student_dsts)
    print("")
    print("")
    
    student_goals = []    # Get all student's destinations
    all_goals = Goal.query.filter(Goal.hide==False).all()
    
    for g in std_gts:
        if g in all_goals:
            student_goals.append(g)
    goals_not_of_student = list(set(all_goals).difference(set(student_goals)))  #goals_not_of_student = all_destinations - std_destinations
                                 
    student_todos = []    # Get all student's destinations
    all_todos = Todo.query.filter(Todo.hide==False).all()
    
    for g in std_gts:
        if g in all_todos:
            student_todos.append(g)
    todos_not_of_student = list(set(all_todos).difference(set(student_todos)))  #todos_not_of_student = all_destinations - std_destinations
      
    whos = Accupation.query.all()
    default_who = Accupation.query.filter(Status.body=='default').first()

    statuss = Status.query.all()
    default_status = Status.query.filter(Status.body=='default').first()
        
    whos = Accupation.query.all()
    default_who = Accupation.query.filter(Accupation.body=='default').first()

    tags = Tag.query.all()
    
    std_txts = Std_general_txt.query.filter(Std_general_txt.student_id==std.id).all()

    due_date = date.today()
        
    age_ranges = Age_range.query.order_by(Age_range.title).all()
    tags = Tag.query.order_by(Tag.title).all()

    return render_template('./tree/show_students_tree.html', std=std, student=std,  
                                                        student_dsts=student_dsts, destinations_not_of_student=destinations_not_of_student,
                                                        all_goals=all_goals, student_goals=student_goals, goals_not_of_student=goals_not_of_student,
                                                        all_todos=all_todos, student_todos=student_todos, todos_not_of_student=todos_not_of_student,
                                                        std_txts=std_txts,
                                                        statuss=statuss, default_status=default_status,
                                                        whos=whos, default_who=default_who,
                                                        tags=tags, age_ranges=age_ranges,
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
    destinations_not_of_student = list(set(all_dsts).difference(set(student_dsts)))  #destinations_not_of_student = all_destinations - std_destinations
   
    
    student_goals = []    # Get all student's destinations
    all_goals = Goal.query.filter(Goal.hide==False).all()
    for g in std_gts:
        if g in all_goals:
            student_goals.append(g)
    goals_not_of_student = list(set(all_goals).difference(set(student_goals)))  #goals_not_of_student = all_destinations - std_destinations
                                 
    student_todos = []    # Get all student's destinations
    all_todos = Todo.query.filter(Todo.hide==False).all()
    for g in std_gts:
        if g in all_todos:
            student_todos.append(g)
    todos_not_of_student = list(set(all_todos).difference(set(student_todos)))  #todos_not_of_student = all_destinations - std_destinations
      
    whos = Accupation.query.all()
    default_who = Accupation.query.filter(Status.body=='default').first()

    statuss = Status.query.all()
    default_status = Status.query.filter(Status.body=='default').first()
        
    whos = Accupation.query.all()
    default_who = Accupation.query.filter(Accupation.body=='default').first()

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
 
 
    return render_template('plan_report/plan_report.html', 
                                                        std=std, student=std, 
                                                        student_dsts=student_dsts, destinations_not_of_student=destinations_not_of_student,
                                                        all_goals=all_goals, student_goals=student_goals, goals_not_of_student=goals_not_of_student,
                                                        all_todos=all_todos, student_todos=student_todos, todos_not_of_student=todos_not_of_student,
                                                        std_txts=std_txts,
                                                        statuss=statuss, default_status=default_status,
                                                        whos=whos, default_who=default_who,
                                                        tags=tags, age_ranges=age_ranges,
                                                        due_date=due_date,
                                                        student_staff_teachers=student_staff_teachers,
                                                        profile=profile, prf_subjects=prf_subjects, prf_strengths=prf_strengths, prf_weaknesses=prf_weaknesses )
       
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
    
	if exist_role == 0:   #new Role
		###########################impor pdb;pdb.set_trace()
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
    
    return student_dsts()

    '''
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))
    std_destinations = Destination.query.join(Std_general_txt).filter(Std_general_txt.general_txt_id==Destination.id).filter(Std_general_txt.student_id == std.id).all()
    age_ranges = Age_range.query.order_by(Age_range.title).all()
    tags = Tag.query.order_by(Tag.title).all() 
    
    #DEBUG
    ################################import pdb;;pdb.set_trace()
    #########std.id, prf.id("std, std_destinations: ", std, std_destinations) 
    
    return render_template('./destinations/edit_std_dst_by_tag.html', 
                                                            std=std,
                                                            destinations=std_destinations, 
                                                            age_ranges=age_ranges,
                                                            tags=tags)
                                                                                                                                
	'''																											  		
@std.route('/edit_student_destinations2/edit/<int:selected_student_id>/<int:selected_destination_id>', methods=['GET', 'POST'])
@login_required
def edit_student_destinations2(selected_student_id, selected_destination_id):
	std = student_select2(selected_student_id)
	if selected_destination_id != 0:
		dest = destination_select2(selected_destination_id)
	return redirect(url_for('students.edit_student_destinations'))		


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

    std_dst = Std_general_txt.query.filter(Std_general_txt.student_id==std.id).filter(Std_general_txt.general_txt_id==dst.id).first()
    if std_dst == None:
        std_dst = Std_general_txt(std.id, dst.id)
    if dst not in std.general_txts:
        std.general_txts.append(std_dst)
    if std not in dst.students:
        dst.students.append(std_dst)
      
    dst.selected=False

    db.session.commit() 

    return redirect(url_for('students.edit_student_destinations'))


	
##############START studets stds###############	
	
@std.route('/student_dsts', methods=['GET', 'POST'])
@login_required
def student_dsts():

    
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
    destinations_not_of_student = list(set(all_dsts).difference(set(student_dsts)))  #destinations_not_of_student = all_destinations - std_destinations
           
    student_goals = []    # Get all student's destinations
    all_goals = Goal.query.filter(Goal.hide==False).all()
    
    for g in std_gts:
        if g in all_goals:
            student_goals.append(g)
    goals_not_of_student = list(set(all_goals).difference(set(student_goals)))  #goals_not_of_student = all_destinations - std_destinations
                                 
    student_todos = []    # Get all student's destinations
    all_todos = Todo.query.filter(Todo.hide==False).all()
    for g in std_gts:
        if g in all_todos:
            student_todos.append(g)
    todos_not_of_student = list(set(all_todos).difference(set(student_todos)))  #todos_not_of_student = all_destinations - std_destinations
      
    whos = Accupation.query.all()
    default_who = Accupation.query.filter(Status.body=='default').first()

    statuss = Status.query.all()
    default_status = Status.query.filter(Status.body=='default').first()
        
    tags = Tag.query.all()
    default_tag = Tag.query.filter(Tag.body=='default').first()
    
    std_txts = Std_general_txt.query.filter(Std_general_txt.student_id==std.id).all()


    due_date = date.today()
   
    age_ranges = Age_range.query.order_by(Age_range.title).all()
    tags = Tag.query.order_by(Tag.title).all()


    return render_template('./destinations/table_destinations/edit_all_dsts.html', std=std,  
                                                        student_dsts=student_dsts, destinations_not_of_student=destinations_not_of_student,
                                                        all_goals=all_goals, student_goals=student_goals, goals_not_of_student=goals_not_of_student,
                                                        all_todos=all_todos, student_todos=student_todos, todos_not_of_student=todos_not_of_student,
                                                        std_txts=std_txts,
                                                        statuss=statuss, default_status=default_status,
                                                        whos=whos, default_who=default_who,
                                                        tags=tags, age_ranges=age_ranges,
                                                        due_date=due_date)
                                                
														  		
@std.route('/student_dsts2/<int:selected_student_id>/<int:selected_destination_id>', methods=['GET', 'POST'])
@login_required
def student_dsts2(selected_student_id, selected_destination_id):

    std = student_select2(selected_student_id)
    std = destination_select2(selected_destination_id)

    return student_dsts()


   
##############START match_dst_to_dst ###############	

@std.route('/match_dst_to_std', methods=['POST'])
@login_required
def match_dst_to_std():
    
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('destination.edit_students'))

    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_student_destinations'))		
   
    statuss = Status.query.all()
    
    new_std_dst = Std_general_txt.query.filter(Std_general_txt.student_id == std.id).filter(Std_general_txt.general_txt_id==dst.id).first()
    new_dst = False
    if new_std_dst == None:   #new Std_dst
        new_dst = True
        new_std_dst = Std_general_txt(std.id, dst.id)                
        new_std_dst.general_txt = dst
        new_std_dst.student = std    
        new_std_dst.due_date = request.form.get('due_date') 
       
    sts_title = request.form.get('selected_status')           
    sts = Status.query.filter(Status.title==sts_title).first()     
    new_std_dst.status_id = sts.id
    
    sts_title = request.form.get('selected_who')           
    acc = Accupation.query.filter(Accupation.title==who_title).first()     
    new_std_dst.acc_id = acc.id

    if new_std_dst not in std.general_txts:
        std.general_txts.append(new_std_dst)
    if new_std_dst not in dst.students:
        dst.students.append(new_std_dst)
                    
    dst.selected = False
    db.session.commit() 

    return  redirect(url_for('students.edit_student_destinations')) 
        
		
@std.route('/match_dst_to_std2/<int:selected_dst_id>', methods=['GET', 'POST'])
@login_required
def match_dst_to_std2(selected_dst_id):
    
    dst = destination_select2(selected_dst_id)
    
    return match_dst_to_std()
    
##############END match_dst_to_dst ###############	


			
@std.route('/match_destination_to_student2/<int:selected_destination_id>', methods=['GET', 'POST'])
@login_required
def match_destination_to_student2(selected_destination_id):
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
            
    std_dst = Std_general_txt.query.filter(Std_general_txt.student_id==student.id).filter(Std_general_txt.general_txt_id==destination.id).first()
    if std_dst != None:
        if std_dst in student.general_txts:
            student.general_txts.remove(std_dst)
        if std_dst in destination.students:            
            destination.students.remove(std_dst)
            
    db.session.commit()  

    return redirect(url_for('students.edit_student_destinations')) 
    

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
        return redirect(url_for('students.edit_student_destinations'))
            
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
		tchr = goal_select2(selected_goal_id)
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
        return redirect(url_for('students.edit_student_destinations'))		
           
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
	                           
   
##############START match_goal_to_std ###############	

@std.route('/match_goal_to_std', methods=['POST'])
@login_required
def match_goal_to_std():
   
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
    
    std_goal = Std_goal.query.filter(Std_goal.student_id == std.id).filter(Std_goal.goal_id==goal.id).first()
    new_std = False
    if std_goal == None:   #new Std_goal
        new_std = True
        std_goal = Std_goal(std.id, goal.id)        

    std_goal.goal_title = goal.title
    std_goal.goal_body = goal.body
    
    std_goal.goal = goal
    std_goal.student = std    
    std_goal.general_txt_id = dst.id
        
    sts_title = request.form.get('selected_status')
    sts = Status.query.filter(Status.title==sts_title).first() 
    std_goal.status_id = sts.id
    std_goal.status_title = sts.title
    std_goal.status_color = sts.color
    
    std_goal.due_date = request.form.get('due_date') 
    
    if new_std:
        std.goals.append(std_goal)			
        goal.students.append(std_goal)
              
    goal.selected = False
    #DEBUG
    db.session.commit() 
    db.session.refresh(std)
    db.session.refresh(goal)
    db.session.refresh(std_goal)

    return  redirect(url_for('students.edit_student_goals')) 
        
		
	
@std.route('/match_goal_to_std2/<int:selected_goal_id>', methods=['GET', 'POST'])
@login_required
def match_goal_to_std2(selected_goal_id):
    
    goal = goal_select2(selected_goal_id)
    
    return match_goal_to_std()
    
##############END match_goal_to_std ###############	


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
        return redirect(url_for('students.edit_student_destinations'))		
   
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
        return redirect(url_for('students.edit_student_destinations'))		
        

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
        return redirect(url_for('students.edit_student_destinations'))		

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
	
##############START match_todo_to_std ###############	

@std.route('/match_todo_to_std', methods=['GET', 'POST'])
@login_required
def match_todo_to_std():

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

    sts = Status.query.filter(Status.title==request.form['selected_status']).first()
    if sts != None:
        std_todo.status_id = sts.id
        std_todo.status_title = sts.title
        std_todo.status_color = sts.color

    who = Accupation.query.filter(Accupation.title==request.form['selected_who']).first() 
    if who != None:    
        std_todo.who_id = who.id
        std_todo.who_title = who.title
           
    std_todo.due_date = request.form['due_date']

    if std_todo_is_new:
        db.session.add(std_todo)
        std.todos.append(std_todo)			
        todo.students.append(std_todo)

    std_todo = Std_todo.query.filter(Std_todo.todo_id == todo.id).filter(Std_todo.student_id==std.id).first() 	
    todo.selected = False
    db.session.commit() 
    db.session.refresh(std)
    db.session.refresh(todo)
    db.session.refresh(std_todo)

    return  redirect(url_for('students.edit_student_goals')) 
        
        	
@std.route('/match_todo_to_std2/<int:selected_goal_id>', methods=['GET', 'POST'])
@login_required
def match_todo_to_std2(selected_goal_id):

    todo = todo_select2(selected_todo_id)
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
        

    student_todos = Todo.query.join(Std_todo).filter(Std_todo.general_txt_id==dst.id).filter(Std_todo.student_id==std.id).all()

    return student_todos


@std.route('/try_get_todos_not_of_student', methods=['GET', 'POST'])
@login_required
def try_get_todos_not_of_student():

    #############################import_pdb; pdb.set_trace()
   
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



######### START  student's genearal txt #################################
  
##############START update_std_txt ###############	

@std.route('/update_std_txt', methods=['POST'])
@login_required
def update_std_txt(txt_type):
    
    #FROM https://stackoverflow.com/questions/43811779/use-many-submit-buttons-in-the-same-form
        
    std_txt = Std_general_txt.query.filter(Std_general_txt.selected==True).first()
       
    if std_txt == None:
        flash("Please select a student and a txt to match  first ")
        return redirect(url_for('students.edit_student_destinations'))		
    
      
    general_txt_sts_name = "sts"+ str(std_txt.general_txt_id)
    
    general_txt_date_name = "due_date" + str(std_txt.general_txt_id)
    
    if txt_type == 'todo':
        general_txt_who_name = "who"+ str(std_txt.general_txt_id)
        
    selected_general_txt_status = Status.query.filter(Status.id==request.form[general_txt_sts_name]).first()
    if selected_general_txt_status != None:
        std_txt.status_id = selected_general_txt_status.id  
    general_txt_due_date = request.form[general_txt_date_name]                
    if general_txt_due_date != None:
        std_txt.due_date = general_txt_due_date
        
    if txt_type == 'todo':
        who = Accupation.query.filter(Accupation.id==request.form.get(general_txt_who_name)).first()
        if who != None:
            std_txt.acc_id = who.id
           
    std_txt.selected = False
        
    db.session.commit() 

    return  redirect(url_for('students.edit_student_destinations')) 


@std.route('/update_std_txt2', methods=['GET', 'POST'])
@login_required
def update_std_txt2():
    
    std = Student.query.filter(Student.selected==True).first()
        
    if( int(request.form['txt_type_form_button_name']) % 3 == 0 ):    # case of destination    
        selected_dst_id = request.form['txt_type_form_button_name']
        selected_dst_id = int(int(selected_dst_id)/3)         
         
        dst = Destination.query.filter(Destination.id == selected_dst_id).first()           
        std_gt = attach_gt_to_std(std.id, dst.id)
     
        std_gt = std_general_txt_select2(std.id, selected_dst_id)
                
        return update_std_txt(txt_type='dst')
         
    elif( int(request.form['txt_type_form_button_name']) % 3 == 1 ):    # case of goal    
        selected_goal_id = request.form['txt_type_form_button_name']
        selected_goal_id = int(int(selected_goal_id)/3)
         
        goal = Goal.query.filter(Goal.id == selected_goal_id).first()            
        std_gt = attach_gt_to_std(std.id, goal.id)
             
        std_gt = std_general_txt_select2(std.id, selected_goal_id) 

        return update_std_txt(txt_type='goal')
                       
    elif ( int(request.form['txt_type_form_button_name']) % 3 == 2 ):     # case of todo   
        selected_todo_id = request.form['txt_type_form_button_name']
        selected_todo_id = int((int(selected_todo_id)-1)/3)

        todo = Todo.query.filter(Todo.id == selected_todo_id).first()           
        std_gt = attach_gt_to_std(std.id, todo.id)
            
        std_gt = std_general_txt_select2(std.id, selected_todo_id) 
                
        return update_std_txt(txt_type='todo')
                   
    return update_std_txt()
    
##############END update_std_txt ###############	

########## START attach_gt_to_std #############################

@std.route('/attach_gt_to_std/<int:std_id>/<int:gt_id>', methods=['GET', 'POST'])
def attach_gt_to_std(std_id, gt_id):
        
    ################import pdb; pdb.set_trace()
    
    std_gt = Std_general_txt.query.filter(Std_general_txt.student_id==std_id).filter(Std_general_txt.general_txt_id==gt_id).first()
    if std_gt == None:
        std_gt = Std_general_txt(std_id, gt_id)
        std_gt.editable = True
        std_gt.due_date = date.today()
        db.session.add(std_gt)
        db.session.commit()
        
        sts = Status.query.filter(Status.body=='default').first()
        if sts == None:
            flash ("please create a default status first")
            return render_template('add_status.html')            
        std_gt.status_id = sts.id 
     
        who = Accupation.query.filter(Accupation.body=='default').first()
        if who == None:
            flash ("please create a default accupation first")
            return render_template('add_accupation.html')          
        std_gt.acc_id = who.id 

        gt = General_txt.query.filter(General_txt.id==gt_id).first()        
        std = Student.query.filter(Student.id==std_id).first()
        if std_gt not in gt.students:
            gt.students.append(std_gt)
        if std_gt not in std.general_txts:
            std.general_txts.append(std_gt)
        
    db.session.commit()
    return std_gt    

########## START attach_gt_to_std #############################

######### END  student's genearal txt #################################


##############START update std profile ###############	

@std.route('/update_std_profile', methods=['GET', 'POST'])
@login_required
def update_std_profile():
    
    #FROM https://stackoverflow.com/questions/43811779/use-many-submit-buttons-in-the-same-form
        
    std_profile_part = Std_general_txt.query.filter(Std_general_txt.selected==True).first()
    profile_part = General_txt.query.filter(General_txt.selected==True).first()
    
    if std_profile_part == None:
        flash("Please select a student and a txt to match  first ")
        return redirect(url_for('students.edit_student_destinations'))
		
    ###std.id, prf.id (" std_profile_part:  std_profile_part.id", std_profile_part, std_profile_part.id) 
    ###std.id, prf.id (" profile_part:  profile_part.id", profile_part, profile_part.id) 
    
    std_profile_part.select = False
    profile_part.select = False
    
    return  redirect(url_for('students.edit_student_destinations')) 

##############END update_std_profile_part ###############	


	
################ START studets gts ##################
	
@std.route('/edit_std_gts', methods=['GET', 'POST'])
@login_required
def edit_std_gts(Gt, Gt_sub, Gt_sub_sub, Gt_sub_sub_sub):   # for example: for student_subjects  ==> Gt = 'Subject' stored  gt.gt_type

    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))
        
    ###########################################################
    # Get students gt of Type Gt                              #
    # If there is no one create a new one and attach to std   #
    ###########################################################
    
    std_gts = []                                             
    all_gts  = eval(Gt).query.all()                          
    for std_gt in std.general_txts:
    
        ###########import pdb; pdb.set_trace()
        #print("")
        #print("")
        #print("")
        #print("std_gt.general_txt.gt_type", std_gt.general_txt.gt_type)
        #print("GT eval ", Gt, eval(Gt))
        #print("std_gt.general_txt.gt_type == Gt", std_gt.general_txt.gt_type == Gt)
        #print("std_gt.general_txt.gt_type == eval(Gt)", std_gt.general_txt.gt_type == Gt)
        #print("")
        #print("")
        #print("")
        
        if std_gt.general_txt.gt_type == Gt:
            std_gts.append(std_gt.general_txt)

    ####################import pdb; pdb.set_trace()
    ####print("IN edit_std_gts --- eval(Gt)=:--- GT ---- ", eval(Gt), Gt )
    # Case of no gt to std. find or create default one and attach to std 
    if std_gts == []:
        gt = eval(Gt).query.filter(eval(Gt).selected==True).first() 
        if gt == None:
            gt = eval(Gt).query.filter(eval(Gt).body==str(std.id)).first()
            if gt == None:               
                gt = eval(Gt)('New', str(std.id), get_author_id())
                gt.gt_type = Gt
                db.session.add(gt)                
                db.session.commit()                
                std_gt = attach_gt_to_std(std.id, gt.id)
                
        std_gts.append(gt)
                         
    gts_not_of_student = list(set(all_gts).difference(set(std_gts)))  #main_gts_not_of_student = all_main_gts - std_gts
    
    #print("std_gts", std_gts)
    #print("")
    
    # Get gt's categories
    gt_categories = []  
    for std_gt in std_gts:    
        for x in get_categories_of(std_gt):
            if x not in gt_categories:
                gt_categories.append(x)

    ###############import pdb; pdb.set_trace()
    
    ##################################################################                                
    ######### Level2 -- Gt's children of Type in Categories ##########
    ##################################################################     
    gt_subs = []
    for gt in std_gts: 
        gt_subs.extend(get_gt_all_categories_children(gt))  

    gt_subs_not_of_std = get_gt_all_categories_children_not_of_std(std, gt)  #main_gts_not_of_student = all_main_gts - std_gts
    
    #NOT OF DEBUG
    
    #print("gt_subs : ", gt_subs)
    #print("")
    #print("gt_subs_not_of_std : ",gt_subs_not_of_std)
  
    
    #NOT OF DEBUG
            
    ##################################################################                                
    ######### Level3 -- Gt's children of Type in Categories ##########
    ##################################################################        
    gt_sub_subs = []
    gt_sub_subs_not_of_std = []
    if Gt_sub_sub != 'None':
        for gt in gt_subs: 
            gt_sub_subs.extend(get_gt_all_categories_children(gt))  
        
        gt_subs_not_of_std = get_gt_all_categories_children_not_of_std(std, gt)  #main_gts_not_of_student = all_main_gts - std_gts
   
    ##################################################################                                
    ######### Level4 -- Gt's children of Type in Categories ##########
    ##################################################################        
    gt_sub_sub_subs = []
    gt_sub_sub_subs_not_of_std = []
    if Gt_sub_sub_sub != 'None':
        for gt in gt_sub_subs: 
            gt_sub_sub_subs.extend(get_gt_all_categories_children(gt))  
        gt_sub_sub_subs_not_of_student = get_gt_all_categories_children_not_of_std(std, gt)  #main_gts_not_of_student = all_main_gts - std_gts

    ####print("gt_sub_subs", gt_sub_sub_subs)
    ####print("")
    
    whos = Accupation.query.all()
    default_who = Accupation.query.filter(Status.body=='default').first()

    statuss = Status.query.all()
    default_status = Status.query.filter(Status.body=='default').first()
        
    tags = Tag.query.all()
    default_tag = Tag.query.filter(Tag.body=='default').first()
    
    std_txts = Std_general_txt.query.filter(Std_general_txt.student_id==std.id).all()


    due_date = date.today()
  
    age_ranges = Age_range.query.order_by(Age_range.title).all()
    tags = Tag.query.order_by(Tag.title).all()

    print("")
    print("")
    print("IN edit_std_gts, BEFORE calling edit_all_main_gts.html --- gt_subs: ", gt_subs)
    print("")
    print("")
    
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
def edit_std_gts2(selected_student_id, selected_gt_id):

    std = student_select2(selected_student_id)
    gt = gt_select2(selected_gt_id)
      
    return edit_std_gts()


 														  		
@std.route('/get_std_gt/<int:std_id>', methods=['GET', 'POST'])
@login_required
def get_std_gt(std_id, Gt):
    
    #print(" IN get_std_gt   std_id Gt ", std_id, Gt)
    ######import pdb; pdb.set_trace()
    
    gt = None
    all_std_gts = Std_general_txt.query.filter(Std_general_txt.student_id==std_id).all()
    all_type_gts = eval(Gt).query.all()
       
    for type_gt in all_type_gts:
        for std_gt in all_std_gts:
            if std_gt.general_txt in all_type_gts:
                gt = std_gt.general_txt  

    
    if gt == None:     # std has no Type gt: ==> Create one
        new_gt = eval(Gt)("New", str(std_id), get_author_id())
        new_gt.gt_type=Gt
        db.session.add(new_gt)
        db.session.commit()
        gt = new_gt
        std_gt = attach_gt_to_std(std_id, gt.id)
        
    std_gt = std_general_txt_select2(std_id, gt.id)
    
    ##print("IN END OF get_std_gt")
    ##print(" std_id, Gt , std_gt, std_gt", std_id, Gt , std_gt, std_gt)
    ##print("")
    ##print("")
    ##print("")
    
    return gt
    
################ END studets gts ##################



################ START studets PROFILE ##################

@std.route('/get_default_prf/<int:selected_profile_id>', methods=['GET', 'POST'])
def get_prf(selected_profile_id):

    author_id = current_user._get_current_object().id
    
    prf = Profile.query.filter(Profile.id == selected_profile_id).first()
       
    if prf == None:
        default_prf = Profile.query.filter(Profile.title=='general').first()
        if default_prf == None:
            default_prf = Profile('general', 'default', author_id)	
            db.session.add(default_prf)
            std = get_dummy_student()   # Match new general prf to Humpty Dumpty
            std_gt = attach_gt_to_std(std.id, default_prf.id)
            db.session.commit()
            
    prf = default_prf


    prf = profile_select2(prf.id)
          
    return prf
    
    	
@std.route('/student_gts', methods=['GET', 'POST'])
@login_required
def edit_std_profile(): 
  
    # for example: for student_subjects  ==> Gt = 'Subject' stored  gt.gt_type
    #DEBUG ONLY
    #DEBUG ONLY
    
    return  edit_std_gts('Profile', 'Subject', 'None', 'None')
                                                    
														  		
@std.route('/edit_std_profile2/<int:selected_student_id>', methods=['GET', 'POST'])
@login_required
def edit_std_profile2(selected_student_id):
        
    std = student_select2(selected_student_id)
            
    ######import pdb; pdb.set_trace()
    
    prf = get_std_gt(std.id, 'Profile')  # Try to get student's profile
    prf = profile_select2(prf.id)
    
    ##print(" IN edit_std_profile2 prf: ", prf, prf.id)
    
    return edit_std_profile()
  
    
  
################ END studets PROFILE ##################
	 
     
@std.route('/get_gt_categories_children', methods=['GET', 'POST'])
@login_required
def get_gt_all_categories_children(gt):  

    ##############import pdb; pdb.set_trace()
     
    # Get gt's categories
    gt_categories = []    
    for x in get_categories_of(gt):
        if x not in gt_categories:
            gt_categories.append(x)

    ####print("IN get_gt_categories_children -- gt_categories --: ", gt_categories)
    ####print("")
       
    gt_all_categories_subs = []
    for ctg in gt_categories:
     
       gt_all_categories_subs.extend(get_gt_children_of_category(gt, ctg)) 
   
    print("")
    print("")
    print("IN get_gt_categories_children -- gt_all_categories_subs --: ", gt_all_categories_subs)
    print("")
    
    return gt_all_categories_subs
 
 
@std.route('/get_gt_children_of_category', methods=['GET', 'POST'])
@login_required
def get_gt_children_of_category(gt, Ctg):

    ###########import pdb; pdb.set_trace()
    print("gt", gt)
    print("")
    print("gt.id", gt.id)
    print("")
    print("gt.gt_type", gt.gt_type)
    print("")
    print("gt.type", gt.type)
    print("")
    print("Ctg", Ctg)
    print("")
    print("Ctg.gt_type", Ctg.gt_type)
    print("")
     
    #import pdb; pdb.set_trace()
    gt_ctg_children = []
    #all_ctg_gts = Ctg.query.all()   # Example: Get all Subjects/Weaknesses/Strengths
    all_ctg_gts = General_txt.query.filter(General_txt.type== Ctg.gt_type.lower()).all()  # Example: Get all Subjects/Weaknesses/Strengths
    for c in gt.children.all():
        if c in all_ctg_gts:
            gt_ctg_children.append(c) 

    print(" IN f", gt_ctg_children)
    print("")
    print("")
    
    return gt_ctg_children

	 
     
@std.route('/get_gt_all_categories_children_not_of_std', methods=['GET', 'POST'])
@login_required
def get_gt_all_categories_children_not_of_std(std, gt):  

    ####import pdb; pdb.set_trace()
    
    # Get gt's categories
    gt_categories = []    
    for x in get_categories_of(gt):
        if x not in gt_categories:
            gt_categories.append(x)

    #print("IN get_gt_all_categories_children_not_of_std -- gt_categories --: ", gt_categories)
    #print("")
    #############import pdb; pdb.set_trace()
    
    gt_all_categories_subs_not_of_std = []
    for ctg in gt_categories:
        gt_all_categories_subs_not_of_std.extend(get_gt_children_of_category_not_of_std(std, ctg.class_name)) 
    
    print("IN get_gt_all_categories_children_not_of_std -- gt_all_categories_subs_not_of_std --: ", gt_all_categories_subs_not_of_std)
    print("")
    
    return gt_all_categories_subs_not_of_std
 
 
@std.route('/get_gt_children_of_category_not_of_std', methods=['GET', 'POST'])
@login_required
def get_gt_children_of_category_not_of_std(std, Ctg):
        
    ###import pdb; pdb.set_trace()
    
    gt_ctg_children_not_of_std = []
    
    all_ctg_gts =   General_txt.query.filter(General_txt.type==Ctg.lower()).all()
    
    #std_gts = Std_general_txt.query.with_entities(Std_general_txt.general_txt).filter(Std_general_txt.student_id==std.id).all()
    
    std_gts = General_txt.query.join(Std_general_txt).filter(Std_general_txt.student_id==std.id).all()
   
    #print("IN LINE 2148:",all_ctg_gts)
    #print("")
   
    #print("IN IN LINE 2151 std std_gts:",std_gts)
    #print("")
   
    gt_ctg_children_not_of_std = list(set(all_ctg_gts).difference(set(std_gts)))  #x_not_of_student = all_x - std_x
    
    '''
    for ctg_gt in all_ctg_gts:
        for std_gt in std_gts:        
            if ctg_gt not in std_gts:
                ###print("ctg_gt: ", ctg_gt)
                ###print("")
                gt_ctg_children_not_of_std.append(ctg_gt) 
    '''
    ###print(" IN get_gt_children_of_category_not_of_std", gt_ctg_children_not_of_std)
    
    return gt_ctg_children_not_of_std

#***********************************************

    ############## START UPDATE STD GT ################

@std.route('/update_std_gt', methods=['POST'])
@login_required
def update_std_gt():
     
    ##print(" IN update_std_gt:")
    ##print("")
    
    ################import pdb; pdb.set_trace()
        
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))
    
   
    std_prf = get_std_gt(std.id, 'Profile')
    ##print(" IN update_std_gt std profile: ", std_prf)
    
    gt = General_txt.query.filter(General_txt.selected == True).filter(General_txt.type!='profile').first()           
    
    std_gt = Std_general_txt.query.filter(Std_general_txt.student_id==std.id).filter(Std_general_txt.general_txt_id==gt.id).first()
    if std_gt == None:    
        ##print(" attaching std.id to gt.id", std.id, gt.id)
        ##print("")
        std_gt = attach_gt_to_std(std.id, gt.id)
     
    ################import pdb; pdb.set_trace()
    ##print(" IN update_std_gt setting gt to be a child of orf profile", gt, std_prf)
    ##print("")
    ##print("")
    
    std_prf.set_parent(gt)

    gt.selected = False
        
    db.session.commit() 

    return  redirect(url_for('students.edit_std_profile2', selected_student_id=std.id )) 


@std.route('/update_std_gt2', methods=['GET', 'POST'])
@login_required
def update_std_gt2():
    
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))
        
    gt_id = int(request.form['save_gt'])    
    
    
    current_prf = Profile.query.filter(Profile.selected==True).first()
        
    ##print("IN update_std_gt2  current_prf", current_prf)
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
    
