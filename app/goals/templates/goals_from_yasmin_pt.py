from flask import render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from flask import render_template, flash, redirect, session, url_for, request, jsonify, json
from flask_login import login_user, logout_user, current_user, login_required
#from flask_login import login_manager
from flask import render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from flask import render_template, flash, redirect, session, url_for, request, jsonify, json
from flask_login import login_user, logout_user, current_user, login_required
#from flask_login import login_manager

from flask_login import LoginManager
from config import basedir
import config

from app import current_app, db
from app.forms import LoginForm

from app.models import User, School, Student, Teacher
from app.models import Profile, Strength, Weakness, Subject
from app.models import Destination, Goal, Todo
from app.models import Resource, Document, Ufile
from app.models import Accupation, Status, Scrt, Tag
from app.models import General_txt, Std_general_txt

from app.forms import LoginForm, EditForm

from app.students.students import get_dummy_student, attach_gt_to_std
from app.gts.gts import gt_delete_for_good2

from sqlalchemy import update

from app.content_management import Content


### For cascade dropdown FROM https://github.com/PrettyPrinted/dynamic_select_flask_wtf_javascript
from flask import jsonify
from flask_wtf import FlaskForm 
from wtforms import SelectField

from datetime import datetime, date

#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
from flask import Blueprint
goal = Blueprint(
    'goals', __name__,
    template_folder='templates'
)   
#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
from app.select.select import profile_select2, strength_select2, destination_select2, goal_select2 
from app.select.select import resource_select2, todo_select2, status_select2, file_select2
from app import *


#update selected goal
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@goal.route('/goal2/update/<int:selected_goal_id>', methods=['GET', 'POST'])
def goal_update(selected_goal_id):

    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        std = get_dummy_student()     # no student is selected goal update is called from destination 

    destination = Destination.query.filter(Destination.selected==True).first()
    print(destination.title)
    if destination == None:
        flash("Please select a destination first ")
        return redirect(url_for('destinations.edit_destinations_goals'))			

    goal = specific_gt_type_select2(selected_general_txt_id, 'Goal')
    print(" IN goal_update selected goal is",goal)
   
    print("student: ", std)
    print("goal: ", goal)

    if request.method == 'GET':
        return render_template('update_goal.html', destination=destination, goal=goal)
        
    #get data from form and insert to destinationgress db
    ###########################import pdb;;pdb.set_trace()
 	
    goal.title = request.form.get('title')	
    goal.body = request.form.get('description')

    db.session.commit()  
    db.session.refresh(goal)

    return redirect(url_for('destinations.edit_destinations_goals'))			
    #end update selected goal 

		
@goal.route('/goal_delete_for_good', methods=['GET', 'POST'])
def goal_delete_for_good():

    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal to delete first ")
        return redirect(url_for('destinations.edit_destinations_goals'))			
            
    print ("delete selected goal is ", goal )
    gt_delete_for_good2(goal)
    return redirect(url_for('destinations.edit_destinations_goals'))			
        
#delete from index goals list
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@goal.route('/goal_delete_for_good2/<int:selected_general_txt_id>', methods=['GET', 'POST'])
#Here author is user_id
def goal_delete_for_good2(selected_general_txt_id):

    print ("SSSSSSSSSSSSSelected goal is" )
    goal = goal_select2(selected_general_txt_id)
    print ("delete selected goal is ", goal )
    gt_delete_for_good2(goal)
    return redirect(url_for('destinations.edit_destinations_goals'))			
        
#########################goals


##############START goal's todos###############	

@goal.route('/edit_goal_todos', methods=['GET', 'POST'])
def edit_goal_todos():

    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('select.goal_select'))	

    print("In edit_goal_todos goal id : ", goal.id )
    
    return render_template('edit_goal_todos.html', goal=goal) 
                                                                
														  		
@goal.route('/edit_goal_todos2/<int:selected_goal_id>', methods=['GET', 'POST'])
def edit_goal_todos2(selected_goal_id):
    print("In edit_goal_todos2 Request is :", request)
    dst = goal_select2(selected_goal_id)
    return redirect(url_for('goals.edit_goal_todos'))		


################## START  Update todo ################    
@goal.route('/goal_todo_update', methods=['GET', 'POST'])
def goal_todo_update():
           
    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('destinations.edit_destinations_goals'))	
        
    todo = Todo.query.filter(Todo.selected==True).first()
    if todo == None:
        flash("Please select a todo first ")
        return redirect(url_for('goals.edit_goal_todos'))		
 
    print ("In  goal_todo_update goal: ",goal, todo )


    form = Todo_form()

    form.title = todo.title
    form.body =  todo.body
    
    form.who.choices=[]
    form.status.choices=[]
    
    form.who.choices = [(acc.id, acc.title) for acc in Accupation.query.all()]
    todo_acc = Accupation.query.join(Todo).filter(Accupation in Todo.children).first()
    form.who.default = todo_acc.id
    
    form.status.choices = [(sts.id, sts.title) for sts in Status.query.all()]
    sts = Status.query.join(Todo).filter(Status in Todo.children).first()
    form.who.default = sts.id
         
    sts_color =  '#ffffcc'
    if sts != None:
        if sts.color != None:
            sts_color = sts.color
                
    ### GET Case
    if request.method == 'GET': 
        return render_template('update_todo.html', form=form, sts_color=sts_color)  
        
    ### POST Case
    ### FROM https://stackoverflow.com/questions/28209131/wtforms-post-with-selectfield-not-working
    print ("form.validate_on_submit", form.validate_on_submit)

    if not form.validate_on_submit:
        flash("יש לבחור קטגוריה")
        return render_template('dsply_todo_form.html', form=form)
        
    ##################  Fill todo fields 
    #######################import pdb;;pdb.set_trace()


    todo.general_txt_id = goal.id
    todo.title = request.form['title'] 
    todo.body =  request.form['body']
    
    ####################import pdb;; pdb.set_trace()
    status = Status.query.filter(Status.id==request.form.get('status')).first()
    todo.status_id = status.id        
    todo.status_title = status.title
    todo.status_color = status.color
  
    
    acc = Accupation.query.filter(Accupation.id==request.form.get('who')).first()
    todo.who_id =  acc.id
    todo.who_title = acc.title

    ##################  Fill todo fields   
                
    db.session.commit()  
    db.session.refresh(todo)
    
    return redirect(url_for('goals.edit_goal_todos' ))   
                                                        
################## START  Update todo ################    


@goal.route('/goal_todo_update2/<int:selected_todo_id>', methods=['GET', 'POST'])
def goal_todo_update2(selected_todo_id):

    print("In UUUUUUUUUU 222222222222 goal_todo_update2 selected_todo_id ", selected_todo_id)
    
    todo = todo_select2(selected_todo_id)
    return redirect(url_for('goals.goal_todo_update'))			


################## START  Add todo ################      
@goal.route('/todo_to_goal_add', methods=['GET', 'POST'])
def todo_to_goal_add():
    print ("In todo_to_goal_add  ")
    
    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a destination first ")
        return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=3))		

    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('destinations.edit_destinations_goals'))		

    form = Todo_form()

    form.who.choices=[]
    form.status.choices=[]

    form.who.choices = [(acc.id, acc.title) for acc in Accupation.query.all()]
    form.process()

    form.status.choices = [(sts.id, sts.title) for sts in Status.query.all()]
    form.process()

    form.due_date = datetime.today()
    form.process()

    first_sts = Status.query.first()

    ### GET Case
    if request.method == 'GET':
        return render_template('todo_to_goal_add.html', goal=goal, form=form)
   

    ### POST Case
    ### FROM https://stackoverflow.com/questions/28209131/wtforms-post-with-selectfield-not-working
    print ("form.validate_on_submit", form.validate_on_submit)

    if not form.validate_on_submit:
        flash("יש לבחור קטגוריה")
        return render_template('todo_to_goal_add.html', form=form)
        
    ########################import pdb;;pdb.set_trace()
                   
    author_id = current_user._get_current_object().id  

    todo = Todo(request.form['title'], request.form['body'], author_id)        
        
    print("todo.children, todo.children.all(): ", goal.children, goal.children.all() )
    if todo not in goal.children.all():
        goal.children.append(todo)
    
    ### asign TO  HUMPTY DUMPTY THE NEW TODO
    hd = get_dummy_student()
    std_gt = attach_gt_to_std(hd.id, todo.id) 
               
    db.session.add(todo)
        
    print(" todo, std_gt:  ", todo, std_gt )
            
    db.session.commit()  
    db.session.refresh(todo)
    
    ########import pdb;; pdb.set_trace()


    return redirect(url_for('goals.edit_goal_todos'))		

                                                    
################## START  Add todo ################    


@goal.route('/todo_to_goal_add2/<int:selected_general_txt_id>', methods=['GET', 'POST'])
def todo_to_goal_add2(selected_general_txt_id):
	print(selected_general_txt_id)
	goal = goal_select2(selected_general_txt_id)
	return redirect(url_for('goals.todo_to_goal_add'))			

	
@goal.route('/todo_from_goal_delete', methods=['GET', 'POST'])
def todo_from_goal_delete():
	
    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('select.goal_select'))		

    todo = Todo.query.filter(Todo.selected==True).first()
    if todo == None:
        flash("Please select a todo to delete first ")
        return redirect(url_for('goals.edit_goal_todos'))
            
    print ("delete selected todo is " + todo.title + " from slected goal " + goal.title )

    goal.children.remove(todo)
    db.session.commit()  

    return redirect(url_for('goals.edit_goal_todos')) 
 
 
@goal.route('/todo_from_goal_delete2/<int:selected_goal_id>/<int:selected_todo_id>', methods=['GET', 'POST'])
def todo_from_goal_delete2(selected_goal_id, selected_todo_id):

    print("totdo id: ", selected_todo_id)
    todo = todo_select2(selected_todo_id)
      
    goal = goal_select2(selected_goal_id)
              
    return redirect(url_for('goals.todo_from_goal_delete')) 	

##############goal's todos ###############	



##############goal's files ###############


@goal.route('/edit_goal_files', methods=['GET', 'POST'])
def edit_goal_files():

    all_files = Ufile.query.all()   #Reset files selection
    for f in all_files:
        f.selected = False
        
    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('destinations.edit_destination_goals'))	

    goal_files = []
    for c in goal.children.all():
        if c.type=='resource':
            if c.ufile_id != None:
                r_file = Ufile.query.filter(Ufile.id==c.ufile_id).first()
                print("")
                print("IN edit_goal_files setting goal_files-- ", r_file, r_file.id)
                print("")
                goal_files.append(r_file)
                
    print("In edit_goal_files student goal goal_files: ", goal, goal_files )
    print("")
    return render_template('edit_goal_files.html', goal=goal, goal_files=goal_files) 
                                                                
														  		
@goal.route('/edit_goal_files2/<int:selected_goal_id>', methods=['GET', 'POST'])
def edit_goal_files2(selected_goal_id):
	print("In edit_goal_files2 Request is :", request)
	goal = goal_select2(selected_goal_id)
	return redirect(url_for('goals.edit_goal_files'))		


from io import BytesIO
from flask.helpers import send_file
	
@goal.route('/download_goal_file', methods=['GET', 'POST'])
def download_goal_file():

    print("IN in download_resource_file")
    print("")
    print("")
    
    author_id = current_user._get_current_object().id
    
    ######import pdb; pdb.set_trace()

    downloaded_file = Ufile.query.filter(Ufile.selected==True).first() 
    if downloaded_file == None:
        flash("Please select a file to download first ")
        return redirect(url_for('goals.edit_goal_files'))	
    
    '''
    resource = Resource.query.filter(Resource.ufile_id==ufile.id).first()
    if resource == None:
        flash("Please select a resource first ")
        return redirect(url_for('goals.edit_goal_files'))	
    '''
    ###import pdb; pdb.set_trace()
    
    downloaded_file =  send_file(BytesIO(downloaded_file.data), attachment_filename=downloaded_file.name, as_attachment=True)
    return downloaded_file
 
        
@goal.route('/download_goal_file2/<int:selected_file_id>', methods=['GET', 'POST'])
def download_goal_file2(selected_file_id):
    ###import pdb; pdb.set_trace()
    print("IN download_goal_file2 selected_file_id: ", selected_file_id)
    print("")
    print("")
    downloded_file = file_select2(selected_file_id)
    return redirect(url_for('goals.download_goal_file'))	

		
@goal.route('/uploaded_file_from_goal_remove', methods=['GET', 'POST'])
def uploaded_file_from_goal_remove():

    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('destinations.edit_destination_goals'))	

    removed_file = Ufile.query.filter(Ufile.selected==True).first()
    if removed_file == None:
        flash("Please select a uploaded_file to delete first ")
        return redirect(url_for('goals.edit_goal_files'))	
    
    resource = Resource.query.filter(Resource.ufile_id==removed_file.id).first()
    if resource == None:
        flash("Please select a resource first ")
        return redirect(url_for('goals.edit_goal_files'))		
    
    goal.unset_parent(resource)    
    db.session.commit()  
    flash("קובץ" + removed_file.name + "הוסר מהיעד בהצחה")
    return redirect(url_for('goals.edit_goal_files'))	


@goal.route('/uploaded_file_from_goal_remove2/<int:selected_file_id>', methods=['GET', 'POST'])
def uploaded_file_from_goal_remove2(selected_file_id):
    
    uploaded_file = file_select2(selected_file_id)
    return redirect(url_for('goals.uploaded_file_from_goal_remove')) 

	
@goal.route('/upload_new_file', methods=['GET', 'POST'])
def upload_new_file():

    ###import pdb; pdb.set_trace()
    
    author_id = current_user._get_current_object().id

    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('goals.edit_goal_files'))	
            
    ##import pdb; pdb.set_trace()
    
    uploaded_file = Ufile.query.filter(Ufile.selected==True).first()
    if uploaded_file == None:
        flash("Please select a file to upload first ")
        return redirect(url_for('goals.edit_goal_files'))	

    print("")
    print("")
    print("IN upload_new_file --- uploaded_file is: ", uploaded_file.id, uploaded_file)
    print("")
    print("")
    
    # Match the new file to a  (created if does'nt exist) resource
    resource = Resource.query.filter(Resource.ufile_id==uploaded_file.id).first()
    if resource == None:

        file_name = uploaded_file.name
        file_data = "The Data is in Ufile"
        file_body = uploaded_file.body
        
        resource = Resource(file_name, file_data, author_id) 
        resource.body = file_body
        db.session.add(resource)
        db.session.commit()

    resource.ufile_id = uploaded_file.id 
    goal.set_parent(resource)

    db.session.commit()  

    print("")    
    print("Uloading a new file to goal: ", goal, goal.id)
    print("goal_upload_new_file uploaded file is: ", uploaded_file, uploaded_file.id)
    print("")
    print("")
    return redirect(url_for('goals.edit_goal_files'))	

@goal.route('/upload_new_file2/<int:selected_goal_id>', methods=['GET', 'POST'])
def upload_new_file2(selected_goal_id):

    print("in upload_new_file2 selected_goal_id is: ", selected_goal_id)
    
    author_id = current_user._get_current_object().id
    
    goal = goal_select2(selected_goal_id)
    
    if request.method == 'GET':
        return render_template('upload_new_file.html', goal=goal)

    uploaded_file = request.files.get('file_name')  # probably can be done only in post upload_new_file2
    file_body = request.form['body']  
    file_name = uploaded_file.filename
    file_data = uploaded_file.read()

    uploaded_file = Ufile.query.filter(uploaded_file.name == file_name).first()
    if uploaded_file == None:
        uploaded_file = Ufile(file_name, file_data, author_id)  #find out how to set file_data
        uploaded_file.body = file_body
        db.session.add(uploaded_file)
        db.session.commit()
        print("")
        print("")
        print(" in upload_new_file2 new file id: ", uploaded_file.id)
    
    uploaded_file = file_select2(uploaded_file.id)
    return redirect(url_for('goals.upload_new_file' ))
               

@goal.route('/replace_uploaded_file2/<int:selected_replaced_file_id>', methods=['GET', 'POST'])
def replace_uploaded_file2(selected_replaced_file_id):

    print("in goal_upload_new_file2 selected_replaced_file_id is: ", selected_replaced_file_id)
    
    author_id = current_user._get_current_object().id

    replaced_file = Ufile.query.filter(Ufile.id==selected_replaced_file_id).first()
    
    print("")
    print("request.method " , request.method )
    print("")
    
    if request.method == 'GET':
        return render_template('replace_uploaded_file.html', replaced_file=replaced_file)


    #remove replaced file 
    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('goals.edit_goal_files'))	      
    resource = Resource.query.filter(Resource.ufile_id==replaced_file.id).first()
    if resource == None:
        flash("Please select a resource first ")
        return redirect(url_for('goals.edit_goal_files'))		    
    goal.unset_parent(resource)    
    db.session.commit() 

    # Uplaod new file
    uploaded_new_file = request.files.get('new_file_name')  # Can be done only here scince it has to be in a post request
    file_body = request.form['body']  
    file_name = uploaded_new_file.filename
    file_data = uploaded_new_file.read()

    uploaded_new_file = Ufile.query.filter(Ufile.name == file_name).first()
    if uploaded_new_file == None:
        uploaded_new_file = Ufile(file_name, file_data, author_id)  #find out how to set file_data
        db.session.add(uploaded_new_file)
        db.session.commit()
    
    uploaded_new_file.name = file_name
    uploaded_new_file.body = file_body
    uploaded_new_file.data = file_data
    
    print("")
    print("")
    print(" in upload_new_file2 new file id: ", uploaded_new_file.id,     uploaded_new_file.name, uploaded_new_file.body)
    print("")
 
    # Match the new uploaded file to a  (created if does'nt exist) resource
    resource = Resource.query.filter(Resource.ufile_id==uploaded_new_file.id).first()
    if resource == None:
        resource = Resource(file_name, file_body, author_id) 
        
        db.session.add(resource)
        db.session.commit()

    resource.ufile_id = uploaded_new_file.id 
    goal.set_parent(resource)

    db.session.commit()  

    print("")    
    print("Uloading a new file to goal: ", goal, goal.id)
    print("goal_upload_new_file uploaded file is: ", uploaded_new_file, uploaded_new_file.id)
    print("")
    print("")
    return redirect(url_for('goals.edit_goal_files'))	

		
##############goal's files ###############	
