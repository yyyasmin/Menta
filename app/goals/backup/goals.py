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

from app.models import User, School, Student, Teacher, Profile, Strength, Weakness, Todo, Resource
from app.models import Std_resource

from app.forms import LoginForm, EditForm

from app.students.students import get_dummy_student

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
from app.select.select import profile_select2, strength_select2, destination_select2, goal_select2, resource_select2, todo_select2, status_select2
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

    goal = goal_select2(selected_general_txt_id)
    print(" IN goal_update selected goal is",goal)
   
    print("student: ", std)
    print("goal: ", goal)

    if request.method == 'GET':
        return render_template('update_goal.html', destination=destination, goal=goal)
        
    #get data from form and insert to destinationgress db
    ###################import pdb;pdb.set_trace()
 	
    goal.title = request.form.get('title')	
    goal.body = request.form.get('description')

    db.session.commit()  
    db.session.refresh(goal)

    return redirect(url_for('destinations.edit_destinations_goals'))			
    #end update selected goal 

		
@goal.route('/goal_delete_for_good', methods=['GET', 'POST'])
def goal_delete_for_good():

    user = User.query.get_or_404(current_user.id)
    author_id = user.id

    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal to delete first ")
        return redirect(url_for('destinations.edit_destinations_goals'))			
            
    print ("delete selected goal is ", goal )

    db.session.delete(goal) 

    db.session.commit()  

    return redirect(url_for('destinations.edit_destinations_goals'))			
        
#delete from index goals list
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@goal.route('/goal_delete_for_good2/<int:selected_general_txt_id>', methods=['GET', 'POST'])
#Here author is user_id
def goal_delete_for_good2(selected_general_txt_id):

	print ("SSSSSSSSSSSSSelected goal is" )
	goal_select2(selected_general_txt_id)
	return redirect(url_for('goals.goal_delete_for_good')) 	
		
#########################goals


##############goal's resources###############	

@goal.route('/edit_goal_resources', methods=['GET', 'POST'])
def edit_goal_resources():

	goal = Goal.query.filter(Goal.selected==True).first()
	if goal == None:
		flash("Please select a goal first ")
		return redirect(url_for('select.edit_destination_goals'))	
        
	print("In edit_goal_resources student for show tree: " )
	return render_template('edit_goal_resources.html', goal=goal) 
																
														  		
@goal.route('/edit_goal_resources2/<int:selected_goal_id>', methods=['GET', 'POST'])
def edit_goal_resources2(selected_goal_id):
	print("In edit_goal_resources2 Request is :", request)
	goal = goal_select2(selected_goal_id)
	return redirect(url_for('goals.edit_goal_resources'))		

	
@goal.route('/resource_to_goal_add', methods=['GET', 'POST'])
def resource_to_goal_add():
    author_id = current_user._get_current_object().id

    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('select.edit_destination_goals'))	

    if request.method == 'GET':
        return render_template('resource_to_goal_add.html', goal=goal)

           
    #get data from form and insert to resourcegress db
    title = request.form.get('title')
    body = request.form.get('description')

    resource = Resource(title, body)

    file_name = request.form.get('file_name')
    uploaded_file = request.files.get('file_name')
    file_name = uploaded_file.filename
    file_data = uploaded_file.read()
    uploaded_file = Ufile(file_name, file_data, author_id)  #find out how to set file_data

    ###################import pdb;pdb.set_trace() 	

    resource.files.append(uploaded_file)

    db.session.add(resource)    	
    goal.resources.append(resource)   
    db.session.commit()  
    db.session.refresh(resource)
    url = url_for('goals.edit_goal_resources' )
    return redirect(url)   

@goal.route('/resource_to_goal_add2/<int:selected_goal_id>', methods=['GET', 'POST'])
def resource_to_goal_add2(selected_goal_id):
	print(selected_goal_id)
	goal = goal_select2(selected_goal_id)
	return redirect(url_for('goals.resource_to_goal_add'))			

	
@goal.route('/resource_from_goal_delete', methods=['GET', 'POST'])
def resource_from_goal_delete():

    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('select.goal_select'))		


    resource = Resource.query.filter(Resource.selected==True).first()
    if resource == None:
        flash("Please select a resource to delete first ")
        return render_template('edit_goal_resources.html', goal=goal) 
            
    print ("delete selected resource is " + resource.title + " from slected goal " + goal.title )

    goal.resources.remove(resource)
    db.session.commit()  

    return redirect(url_for('goals.edit_goal_resources')) 

@goal.route('/resource_from_goal_delete2/<int:selected_general_txt_id><int:selected_resource_id>', methods=['GET', 'POST'])
#Here author is user_id
def resource_from_goal_delete2(selected_general_txt_id, selected_resource_id):
	goal = goal_select2(selected_general_txt_id)

	resource = resource_select2(selected_resource_id)
	return redirect(url_for('goals.resource_from_goal_delete')) 	

############## END goal's resources###############	


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
    ###############import pdb;pdb.set_trace()


    todo.general_txt_id = goal.id
    todo.title = request.form['title'] 
    todo.body =  request.form['body']
    
    ############import pdb; pdb.set_trace()
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
        return redirect(url_for('destinations.edit_destinations'))		

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
        
    ################import pdb;pdb.set_trace()
                   
    author_id = current_user._get_current_object().id  

    todo = Todo(request.form['title'], request.form['body'], author_id)        
        
    todo.parents.append(goal)
    print("todo.children, todo.children.all(): ", goal.children, goal.children.all() )
    goal.children.append(todo)
    
    sts = Status.query.filter(Status.id==request.form.get('status')).first()               
    todo.children.append(status)
    status.parents.append(todo)
                    
    acc = Accupation.query.filter(Accupation.id==request.form.get('who')).first()           
    todo.children.append(acc)                    
    acc.parents.append(todo)                    

    ### asign TO  HUMPTY DUMPTY THE NEW TODO
    std = get_dummy_student() 
    std_todo = Std_general_txt(std.id, todo.id)
    todo.students.append(std_todo)
    std.general_txts.append(std_todo)
        
    db.session.add(todo)
    
    print(" todo, status, sts-color:  ", status, status.color )
            
    db.session.commit()  
    db.session.refresh(todo)
    
    import pdb; pdb.set_trace()


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

##############goal's todos###############	
