from flask import render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, json
from flask_login import login_user, logout_user, current_user, login_required
#from flask_login import login_manager

from flask_login import LoginManager
from config import basedir
import config

from app import current_app, db

from app.models import User, Student, Teacher, Role, School
from app.models import Profile, Strength, Weakness, Subject
from app.models import Accupation, Tag, Scrt, Age_range, Status
from app.models import Resource, Document, Ufile
from app.models import Destination, Goal, Todo 
from app.models import Std_general_txt

from app.forms import LoginForm, EditForm
from app import teachers
from app import students
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

################
#### config ####
################

slct = Blueprint(
    'select', __name__,
    template_folder='templates'
) 
from app import *


#Select a teacher from a list 
@slct.route('/teacher_select2/<int:selected_teacher_id>', methods=['GET', 'POST'])
def teacher_select2(selected_teacher_id):
	
	teachers = Teacher.query.all()
	for teacher in teachers:
		teacher.selected = False

	teacher = Teacher.query.get_or_404(selected_teacher_id)		
		
	teacher.selected = True
	##print(teacher.first_name)
	
	db.session.commit()
	
	teacher = Teacher.query.get_or_404(selected_teacher_id)
	return teacher
	'''
	teachers = Teacher.query.all()
	return render_template('show_teachers.html', teachers=teachers)
	'''
	#Select a teacher from a list 

@slct.route('/student_select2/<int:selected_student_id>', methods=['GET', 'POST'])
def student_select2(selected_student_id):
	
	students = Student.query.all()
	for student in students:
		student.selected = False
	########################import pdb;;; pdb.set_trace()
	student = Student.query.get_or_404(selected_student_id)		
		
	student.selected = True
	##print(student.first_name)
	
	db.session.commit()
	
	student = Student.query.get_or_404(selected_student_id)
	return student
	#Select a student from a list 


#Select a profile from a list 
@slct.route('/profile_select2/<int:selected_profile_id>', methods=['GET', 'POST'])
def profile_select2(selected_profile_id):

    #########import pdb; pdb.set_trace()

    profiles = Profile.query.all()
    for prfl in profiles:
        prfl.selected = False

    profile = Profile.query.get_or_404(selected_profile_id)		
        
    profile.selected = True	
    db.session.commit()

    return profile

#Select a profile from a list 	
	

@slct.route('/destination_select2/<int:selected_destination_id>', methods=['GET', 'POST'])
def destination_select2(selected_destination_id):
    #print(" IIIIIIIIn destination_select2", selected_destination_id)
    destinations = Destination.query.all()
    
    for dst in destinations:
        dst.selected = False
        
    dst = Destination.query.filter(Destination.id==selected_destination_id).first()		
    if dst == None:
        return ("error trying to select a destiantion number: ", selected_destination_id)
        
    #print("IN select -- selected dst is: ", dst)
        
    dst.selected = True

    db.session.commit()

    return dst
    
#####Select a destination from a list 

@slct.route('/accupation_select2/<int:selected_accupation_id>', methods=['GET', 'POST'])
def accupation_select2(selected_accupation_id):
	
    accupations = Accupation.query.all()
    for accupation in accupations:
        accupation.selected = False

    accupation = accupation.query.get_or_404(selected_accupation_id)				
    accupation.selected = True
    db.session.commit()

    return accupation
###Select a accupation from a list 
	
@slct.route('/todo_select2/<int:selected_todo_id>', methods=['GET', 'POST'])
def todo_select2(selected_todo_id):
	
    todos = Todo.query.all()
    for todo in todos:
        todo.selected = False

    todo = Todo.query.filter(Todo.id == selected_todo_id).first()
    if todo==None:
        flash("Please select a todo for thisstudent first")
        redirect(url_for('students.edit_student_todos'))
    
    todo.selected = True
    db.session.commit()

    return todo
###Select a todo from a list 	

###Select a status from a list 	
@slct.route('/status_select2/<int:selected_status_id>', methods=['GET', 'POST'])
def status_select2(selected_status_id):
	
    statuss = Status.query.all()
    for status in statuss:
        status.selected = False

    status = Status.query.get_or_404(selected_status_id)				
    status.selected = True
    db.session.commit()

    return status
###Select a status from a list 	


###Select a school from a list 	
@slct.route('/school_select2/<int:selected_school_id>', methods=['GET', 'POST'])
def school_select2(selected_school_id):
	
    schools = School.query.all()
    for school in schools:
        school.selected = False

    school = School.query.filter(School.id==selected_school_id).first()
    if school == None:
        flash("אין כזה בית ספר")
        redirect(url_for('schools.edit_schools'))
        
    school.selected = True
    db.session.commit()

    return school
###Select a school from a list 	


####Select a age_range ###########################
@slct.route('/age_range_select', methods=['GET', 'POST'])
def age_range_select():
	##print("1111111111111")
	age_ranges = Age_range.query.all()
	for age_range in age_ranges:
		age_range.selected = False
	
	if request.method == 'GET':
		return render_template('edit_age_ranges.html', age_ranges=age_ranges)
		
	##print("1111111111111")
		
	selected_age_range_id = int(request.form['selected_age_range'])
	##print("1111111111111")

	##print ("SSSSSSSSSSSSSelected age_range is" )
	##print (selected_age_range_id)

	age_range = age_range.query.get_or_404(selected_age_range_id)		
		
	age_range.selected = True
	##print(age_range.first_name)
	
	db.session.commit()
	
	age_range = age_range.query.get_or_404(selected_age_range_id)
	##print(age_range.selected)
	age_ranges = age_range.query.all()
	#return render_template('show_selected_age_range.html', age_ranges=age_ranges)
	return edit_age_ranges()
	
@slct.route('/age_range_select2/<int:selected_age_range_id>', methods=['GET', 'POST'])
def age_range_select2(selected_age_range_id):

    age_ranges = Age_range.query.all()
    for age_range in age_ranges:
        age_range.selected = False

    age_range = Age_range.query.filter(Age_range.id==selected_age_range_id).first()		
    if  age_range == None:
        flash("In age_range_select2 --- faled to get age_range id: ", selected_age_range_id)
        redirect(url_for('students.edit_student_destinations'))
    
    age_range.selected = True
    db.session.commit()

    return age_range
####Select a age_range ##########################3
	

####Select a category_select2 ##########################3	
@slct.route('/category_select2/<int:selected_category_id>', methods=['GET', 'POST'])
def category_select2(selected_category_id):

    categories = Category.query.all()
    for category in categories:
        category.selected = False

    category = Category.query.get_or_404(selected_category_id)				
    category.selected = True
    db.session.commit()

    return category	
    
    
####Select a scrt ###########################
@slct.route('/scrt_select', methods=['GET', 'POST'])
def scrt_select():
	##print("1111111111111")
	scrts = Scrt.query.all()
	for scrt in scrts:
		scrt.selected = False
	
	if request.method == 'GET':
		return render_template('edit_scrts.html', scrts=scrts)
		
	##print("1111111111111")
		
	selected_scrt_id = int(request.form['selected_scrt'])
	##print("1111111111111")

	##print ("SSSSSSSSSSSSSelected scrt is" )
	##print (selected_scrt_id)

	scrt = scrt.query.get_or_404(selected_scrt_id)		
		
	scrt.selected = True
	##print(scrt.first_name)
	
	db.session.commit()
	
	scrt = scrt.query.get_or_404(selected_scrt_id)
	##print(scrt.selected)
	scrts = scrt.query.all()
	#return render_template('show_selected_scrt.html', scrts=scrts)
	return edit_scrts()
	
@slct.route('/scrt_select2/<int:selected_scrt_id>', methods=['GET', 'POST'])
def scrt_select2(selected_scrt_id):

    scrts = Scrt.query.all()
    for scrt in scrts:
        scrt.selected = False

    scrt = Scrt.query.get_or_404(selected_scrt_id)				
    scrt.selected = True
    db.session.commit()

    return scrt
####Select a scrt ##########################3
				

@slct.route('/goal_select2/<int:selected_goal_id>', methods=['GET', 'POST'])
def goal_select2(selected_goal_id):

    goals = Goal.query.all()
    for goal in goals:
        goal.selected = False

    goal = Goal.query.filter(Goal.id==selected_goal_id).first()
    if goal == None:
        flash("Please select a goal for student ")
        return redirect(url_for("students.edit_student_goals"))
        
    goal.selected = True
    db.session.commit()

    return goal


############# Std_goal select 
@slct.route('/std_goal_select2/<int:selected_std_id>/<int:selected_goal_id>', methods=['GET', 'POST'])
def std_goal_select2(selected_std_id, selected_goal_id):

    #std_goals = Std_goal.query.all()
    
    std_goals = Std_general_txt.query.filter(Std_general_txt.type=='goal').all()

    for std_goal in std_goals:
        std_goal.selected = False

    std_goal = Std_general_txt.query.filter(Std_general_txt.id == selected_goal_id).filter(Std_general_txt.student_id==selected_std_id).first()
    if std_goal == None:
        flash("Please select a goal for student ")
        return redirect(url_for("students.edit_student_goals"))
        
    std_goal.selected = True
    db.session.commit()

    return std_goal
############# Std_goal select 


@slct.route('/resource_select', methods=['GET', 'POST'])
def resource_select():
	#print("in ppppppppppppppppresource_ssssssssssssssssssselect")

	destination = Destination.query.filter(Destination.selected==True).first()
	if destination == None:
		flash("Please select a destination first ")
		return redirect(url_for('index'))

	goal = Goal.query.filter(Goal.selected==True).first()

	if goal == None:
		flash("Please select an goal first ")
		return redirect(url_for('goal_select'))		
	#print(goal.title)      

	resources = Resource.query.join(Goal.resources).filter(Goal.id==goal.id)	

	if (resources.count() == 0):
		flash("There is no resources for this destination.")
		#print ("resources count is 0 ")
		redirect(url_for('flash_err'))
		return render_template('select_resource.html', resources=resources)
		#return redirect(url_for('index'))

	resource = Resource.query.all()		
	for resource in resources:
		resource.selected = False

	if request.method == 'GET':
		return render_template('select_resource.html', resources=resources)
		
	selected_resource_id = int(request.form['selected_resource'])
	resource = Resource.query.get_or_404(selected_resource_id)
	resource.selected = True
		
	db.session.commit()
	#goals = Goal.query.all()
	return redirect(url_for('goals.edit_goal_resources'))		



@slct.route('/resource_select2/<int:selected_resource_id>', methods=['GET', 'POST'])
def resource_select2(selected_resource_id):

    resources = Resource.query.all()
    for resource in resources:
        resource.selected = False
             
    resource = Resource.query.filter(Resource.id == selected_resource_id).first()
    if resource == None:
        flash("Please select an resource first ")
        return redirect(url_for('resources.edit_resource_uploaded_files'))	
        
    resource.selected = True
    db.session.commit()

    return resource


@slct.route('/document_select2/<int:selected_document_id>', methods=['GET', 'POST'])
def document_select2(selected_document_id):

    docs = Document.query.all()
    for doc in docs:
        doc.selected = False

    doc = Document.query.get_or_404(selected_document_id)
    if doc == None:
        flash("Please select an document first ")
        return redirect(url_for('students.edit_student_documents'))	
    #print("in DDDOOOCCC 222 document_select2 document is: ", doc.id, doc.title)  
    
    doc.selected = True
    db.session.commit()

    return doc


############# Std_strength select 
@slct.route('/std_strength_select2/<int:selected_std_id>/<int:selected_strength_id>', methods=['GET', 'POST'])
def std_strength_select2(selected_std_id, selected_strength_id):

    #std_strengths = Std_strength.query.all()
    
    std_strengths = Std_general_txt.query.filter(Std_general_txt.type=='strength').all()

    for std_strength in std_strengths:
        std_strength.selected = False

    std_strength = Std_general_txt.query.filter(Std_general_txt.id == selected_strength_id).filter(Std_general_txt.student_id==selected_std_id).first()
    if std_strength == None:
        flash("Please select a strength for student ")
        return redirect(url_for("students.edit_student_strengths"))
        
    std_strength.selected = True
    db.session.commit()

    return std_strength
    
############# Std_strength select 



############# Std_weakness select 
@slct.route('/std_weakness_select2/<int:selected_std_id>/<int:selected_weakness_id>', methods=['GET', 'POST'])
def std_weakness_select2(selected_std_id, selected_weakness_id):

    #std_weaknesss = Std_weakness.query.all()
    
    std_weaknesss = Std_general_txt.query.filter(Std_general_txt.type=='weakness').all()

    for std_weakness in std_weaknesss:
        std_weakness.selected = False

    std_weakness = Std_general_txt.query.filter(Std_general_txt.id == selected_weakness_id).filter(Std_general_txt.student_id==selected_std_id).first()
    if std_weakness == None:
        flash("Please select a weakness for student ")
        return redirect(url_for("students.edit_student_weaknesss"))
        
    std_weakness.selected = True
    db.session.commit()

    return std_weakness
############# Std_weakness select 


############# Std_subject select 
@slct.route('/std_subject_select2/<int:selected_std_id>/<int:selected_subject_id>', methods=['GET', 'POST'])
def std_subject_select2(selected_std_id, selected_subject_id):

    #std_subjects = Std_subject.query.all()
    
    std_subjects = Std_general_txt.query.filter(Std_general_txt.type=='subject').all()

    for std_subject in std_subjects:
        std_subject.selected = False

    std_subject = Std_general_txt.query.filter(Std_general_txt.id == selected_subject_id).filter(Std_general_txt.student_id==selected_std_id).first()
    if std_subject == None:
        flash("Please select a subject for student ")
        return redirect(url_for("students.edit_student_subjects"))
        
    std_subject.selected = True
    db.session.commit()

    return std_subject
############# Std_subject select 


@slct.route('/strength_select2/<int:selected_strength_id>', methods=['GET', 'POST'])
def strength_select2(selected_strength_id):

	strengthes = Strength.query.all()		
	for strn in strengthes:
		strn.selected = False

	strn = Strength.query.get_or_404(selected_strength_id)

	strn.selected = True
	db.session.commit()

	return strn	



@slct.route('/weakness_select2/<int:selected_weakness_id>', methods=['GET', 'POST'])
def weakness_select2(selected_weakness_id):

	weaknesses = Weakness.query.all()		
	for wkns in weaknesses:
		wkns.selected = False

	wkns = Weakness.query.get_or_404(selected_weakness_id)

	wkns.selected = True
	db.session.commit()

	return wkns	


@slct.route('/subject_select2/<int:selected_subject_id>', methods=['GET', 'POST'])
def subject_select2(selected_subject_id):

    subjects = Subject.query.all()		
    for sbj in subjects:
        sbj.selected = False

    sbj = Subject.query.filter(Subject.id==selected_subject_id).first()
    if sbj == None:
        flash("Please select a subject plese ")
        return redirect(url_for("profile.edit_profile_by_tag"))

    sbj.selected = True
    db.session.commit()

    return sbj	


@slct.route('/tag_select2/<int:selected_tag_id>', methods=['GET', 'POST'])
def tag_select2(selected_tag_id):
	
    tags = Tag.query.all()
    for tag in tags:
        tag.selected = False

    tag = Tag.query.get_or_404(selected_tag_id)
    if tag == None:
        flash("There is no sush tag ", tag.id, tag.title)
        return redirect(url_for("gts.edit_gts"))

    tag.selected = True		
    db.session.commit()

    tag = Tag.query.filter(Tag.selected==True).first()	

    print("")
    print("In SELECT_TAG AFTER  query tag-id: ", tag.id)	

    return tag


@slct.route('/sub_tag_select2/<int:selected_sub_tag_id>', methods=['GET', 'POST'])
def sub_tag_select2(selected_sub_tag_id):
	
    sub_tags = Sub_tag.query.all()
    for sub_tag in sub_tags:
        sub_tag.selected = False

    sub_tag = sub_tag.query.filter(Sub_tag.id==selected_sub_tag_id).first()
    if sub_tag == None:
        flash("There is no sush sub_tag ", sub_tag.id, sub_tag.title)
        return redirect(url_for("gts.edit_gts"))

    sub_tag.selected = True		
    db.session.commit()

    sub_tag = sub_tag.query.filter(Sub_tag.selected==True).first()	

    print("")
    print("In SELECT_sub_tag AFTER  query sub_tag-id: ", sub_tag.id)	

    return sub_tag


	
#Select a file from a list 
@slct.route('/file_select', methods=['GET', 'POST'])
def file_select():
	##print("1111111111111")
	files = Ufile.query.filter(Ufile.hide == False).all()
	for file in files:
		file.selected = False
	
	if request.method == 'GET':
		return render_template('edit_files.html', files=files)
		
	##print("1111111111111")
		
	selected_file_id = int(request.form['selected_file'])
	##print("1111111111111")

	##print ("SSSSSSSSSSSSSelected file is" )
	##print (selected_file_id)

	file = Ufile.query.get_or_404(selected_file_id)		
		
	file.selected = True
	##print(file.first_name)
	
	db.session.commit()
	
	file = Ufile.query.get_or_404(selected_file_id)
	##print(Ufile.selected)
	files = Ufile.query.filter(file.hide == False).all()
	#return render_template('show_selected_file.html', files=files)
	return edit_resource_uploaded_files()

	
@slct.route('/file_select2/<int:selected_file_id>', methods=['GET', 'POST'])
def file_select2(selected_file_id):
	
    files = Ufile.query.all()
    for file in files:
        file.selected = False

    print("")
    print("")
    print("IN file_select2 selected_file_id is", selected_file_id)
    print("")	

    file = Ufile.query.filter(Ufile.id==selected_file_id).first()
    if file == None:
        flash("Please select a file")
        return redirect(url_for("goals.edit_goal_files"))
            
    file.selected = True		
    db.session.commit()

    return file


@slct.route('/general_txt_select2/<int:selected_general_txt_id>', methods=['GET', 'POST'])
def general_txt_select2(selected_general_txt_id):
    
    general_txt =  General_txt.query.filter( General_txt.id==selected_general_txt_id ).first()
   
    if general_txt == None:
        flash("Please select a general_txt for student ")
        return redirect(url_for("gts.edit_gts"))
             
    general_txts = General_txt.query.all()
    for gt in general_txts:
        gt.selected = False
           
    general_txt.selected = True
    db.session.commit()
    return general_txt

@slct.route('/general_txt_select2/<int:selected_general_txt_id>', methods=['GET', 'POST'])
def gt_type_select2(selected_general_txt_id):
    
    general_txt =  General_txt.query.filter( General_txt.id==selected_general_txt_id ).first()
   
    if general_txt == None:
        flash("Please select a general_txt for student ")
        return redirect(url_for("gts.edit_gts"))
             
    general_txts = General_txt.query.all()
    for gt in general_txts:
        if gt.type==general_txt.type:
            gt.selected = False
           
    general_txt.selected = True
    db.session.commit()
    return general_txt


@slct.route('/specific_gt_type_select2/<int:selected_general_txt_id>', methods=['GET', 'POST'])
def specific_gt_type_select2(selected_general_txt_id, gt_type):
    
    print("IN specific_gt_type_select2 gt_type:  selected_general_txt_id: ", gt_type, selected_general_txt_id )
    
    general_txts = eval(gt_type).query.all()
    for general_txt in general_txts:
        general_txt.selected = False

    general_txt =  eval(gt_type).query.filter( eval(gt_type).id==selected_general_txt_id).first()
    if general_txt == None:
        flash("Please select a general_txt for student ")
        return redirect(url_for("gts.edit_gts"))
        
    general_txt.selected = True
    db.session.commit()

    return general_txt


############# Std_general_txt select 
@slct.route('/std_general_txt_select2/<int:selected_std_id>/<int:selected_general_txt_id>', methods=['GET', 'POST'])
def std_general_txt_select2(selected_std_id, selected_general_txt_id):
    
    std_general_txts = Std_general_txt.query.all()

    for std_general_txt in std_general_txts:
        std_general_txt.selected = False

    std_general_txt = Std_general_txt.query.filter(Std_general_txt.general_txt_id == selected_general_txt_id).filter(Std_general_txt.student_id==selected_std_id).first()
    if std_general_txt == None:
        flash("Please select a general_txt for student ")
        return redirect(url_for("students.edit_student_destinations"))
            
    std_general_txt.selected = True
    db.session.commit()

    return std_general_txt
############# Std_general_txt select 

	
	

