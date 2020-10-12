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

from app.students.students import get_dummy_student, attach_gt_to_std, edit_std_gts, edit_std_gts2
from app.gts.gts import gt_delete_for_good2, set_gt_category
from app.select.select import method_select2, test_select2
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
from app.select.select import resource_select2, todo_select2, status_select2, file_select2, specific_gt_type_select2
from app import *


#update selected goal
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@goal.route('/goal2/update/<int:selected_goal_id>', methods=['GET', 'POST'])
def goal_update(selected_goal_id):

    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        std = get_dummy_student()     # no student is selected goal update is called from destination 

    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a destination first ")
        return redirect(url_for('destinations.edit_destinations_goals'))			

    goal = specific_gt_type_select2(selected_goal_id, 'Goal')
    print(" IN goal_update selected goal is",goal)
   
    print("student: ", std)
    print("goal: ", goal)

    if request.method == 'GET':
        return render_template('update_goal.html', dst=dst, goal=goal)
        
    #get data from form and insert to destinationgress db
    #############################import pdb;;pdb.set_trace()
 	
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

    #####import pdb; pdb.set_trace()
    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a destination first ")
        return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=3))	

    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('destinations.edit_destination_goals'))	

    std = get_dummy_student()
    print("In edit_goal_todos dummy_std   goal id : ", std.id, goal.id )
    return render_template('edit_goal_todos.html', dst=dst, goal=goal)                                             
                                                                
														  		
@goal.route('/edit_goal_todos2/<int:selected_goal_id>', methods=['GET', 'POST'])
def edit_goal_todos2(selected_goal_id):
    print("In edit_goal_todos2 Request is :", request)
    goal = goal_select2(selected_goal_id)
    return redirect(url_for('goals.edit_goal_todos'))		


################## START  Update todo ################    
@goal.route('/goal_todo_update', methods=['GET', 'POST'])
def goal_todo_update():

    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a goal first ")
        return redirect(url_for('destinations.edit_destinations_goals'))	
             
    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('destinations.edit_destinations_goals'))	
        
    todo = Todo.query.filter(Todo.selected==True).first()
    if todo == None:
        flash("Please select a todo first ")
        return redirect(url_for('goals.edit_goal_todos'))		
 
    print ("In  goal_todo_update goal: ", dst, goal, todo )

    #DEBUG ONLY

    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a goal first ")
        return redirect(url_for('destinations.edit_destinations_goals'))	
    #DEBUG ONLY
         
    
    form = Todo_form()

    form.title = todo.title
    form.body =  todo.body
    
    form.who.choices=[]
    form.status.choices=[]
    
    form.who.choices = [(acc.id, acc.title) for acc in Accupation.query.all()]
    for who in Accupation.query.all():
        if todo.is_parent_of(who):
            form.who.default = who.id
            break
    
    form.status.choices = [(sts.id, sts.title) for sts in Status.query.all()]
    for sts in Status.query.all():
        if sts.is_parent_of(sts):
            form.who.default = sts.id
            break
                     
    ### GET Case
    if request.method == 'GET': 
        return render_template('update_todo.html', form=form, dst=dst)  
        
    ### POST Case
    ### FROM https://stackoverflow.com/questions/28209131/wtforms-post-with-selectfield-not-working
    print ("form.validate_on_submit", form.validate_on_submit)

    if not form.validate_on_submit:
        flash("יש לבחור קטגוריה")
        return render_template('dsply_todo_form.html', form=form)
        
    ##################  Fill todo fields 
    #########################import pdb;;pdb.set_trace()

    todo.title = request.form['title'] 
    todo.body =  request.form['body']
    
    who = Accupation.query.filter(Accupation.id==request.form.get('who')).first()
    todo.set_parent(who)
    goal.set_parent(who)
    goal.set_parent(todo)
    
    who=set_gt_category(todo.id, 'Accupation', who.title, "יש לבחור תפקיד אחראי")  

    ##################  Fill todo fields   
                
    db.session.commit()  
    db.session.refresh(todo)
    
    return redirect(url_for('goals.edit_goal_todos', dst=dst ))   
                                                        
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
        return render_template('todo_to_goal_add.html', dst=dst, goal=goal, form=form)
   

    ### POST Case
    ### FROM https://stackoverflow.com/questions/28209131/wtforms-post-with-selectfield-not-working
    print ("form.validate_on_submit", form.validate_on_submit)

    if not form.validate_on_submit:
        flash("יש לבחור קטגוריה")
        return render_template('todo_to_goal_add.html', form=form)
        
    ##########################import pdb;;pdb.set_trace()
                   
    author_id = current_user._get_current_object().id  

    todo = Todo(request.form['title'], request.form['body'], author_id)        
    db.session.add(todo)
        
    print("todo.children ", goal.children )
    
    ### asign TO  HUMPTY DUMPTY THE NEW TODO
    hd = get_dummy_student()
    std_gt = attach_gt_to_std(hd.id, todo.id) 
   
    default_sts = Status.query.filter(Status.default==True).first()    
    todo.set_parent(default_sts)    
    std_gt.status_id = default_sts.id
    
    who = Accupation.query.filter(Accupation.id==request.form.get('who')).first()    
    #who=set_gt_category(todo.id, 'Accupation', who.title, "יש לבחור תפקיד אחראי")  
                       
    goal.set_parent(todo)
    goal.set_parent(who)
    todo.set_parent(who)
            
    db.session.commit()  
    db.session.refresh(todo)
    
    ##########import pdb;; pdb.set_trace()


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





##############START goal's methods###############	

@goal.route('/edit_goal_methods', methods=['GET', 'POST'])
def edit_goal_methods():

    #####import pdb; pdb.set_trace()
    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a destination first ")
        return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=3))	

    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('destinations.edit_destinations_goals'))	

    std = get_dummy_student()
    print("In edit_goal_methods dummy_std   goal id : ", std.id, goal.id )
    return render_template('edit_goal_methods.html', dst=dst, goal=goal)                                             
                                                                
														  		
@goal.route('/edit_goal_methods2/<int:selected_goal_id>', methods=['GET', 'POST'])
def edit_goal_methods2(selected_goal_id):
    print("In edit_goal_methods2 Request is :", request)
    goal = goal_select2(selected_goal_id)
    return redirect(url_for('goals.edit_goal_methods'))		


################## START  Update method ################    
@goal.route('/goal_method_update', methods=['GET', 'POST'])
def goal_method_update():

    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a goal first ")
        return redirect(url_for('destinations.edit_destinations_goals'))	
             
    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('destinations.edit_destinations_goals'))	
        
    method = Method.query.filter(Method.selected==True).first()
    if method == None:
        flash("Please select a method first ")
        return redirect(url_for('goals.edit_goal_methods'))		
 
    print ("In  goal_method_update goal: ", dst, goal, method )

    #DEBUG ONLY

    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a destination first ")
        return redirect(url_for('destinations.edit_destinations_goals'))	
    #DEBUG ONLY
   
    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('destinations.edit_destinations_goals'))	
    #DEBUG ONLY
         
    
    form = Todo_form()

    form.title = method.title
    form.body =  method.body
    
    form.who.choices=[]
    form.method_type.choices=[]
    
    form.who.choices = [(acc.id, acc.title) for acc in Accupation.query.all()]
    for who in Accupation.query.all():
        if method.is_parent_of(who):
            form.who.default = who.id
            break
    
    form.method_type.choices = [(mt.id, mt.title) for mt in Method_type.query.all()]
    for mt in Method_type.query.all():
        if method.is_parent_of(mt):
            form.method_type.default = mt.id
            break
                    
    ### GET Case
    if request.method == 'GET': 
        return render_template('update_method.html', form=form, dst=dst, goal=goal)  
        
    ### POST Case
    ### FROM https://stackoverflow.com/questions/28209131/wtforms-post-with-selectfield-not-working
    print ("form.validate_on_submit", form.validate_on_submit)

    if not form.validate_on_submit:
        flash("יש לבחור קטגוריה")
        return render_template('dsply_method_form.html', form=form)
        
    ##################  Fill method fields 
    #########################import pdb;;pdb.set_trace()

    method.title = request.form['title'] 
    method.body =  request.form['body']
    
    who = Accupation.query.filter(Accupation.id==request.form.get('who')).first()
    method_type = Method_type.query.filter(Method_type.id==request.form.get('method_type')).first()
    
    method.set_parent(who)
    method.set_parent(method_type)
    goal.set_parent(who)
    goal.set_parent(method)
    
    who=set_gt_category(method.id, 'Accupation', who.title, "יש לבחור תפקיד אחראי")  

    ##################  Fill method fields   
                
    db.session.commit()  
    db.session.refresh(method)
    
    return redirect(url_for('goals.edit_goal_methods', dst=dst, goal=goal ))   
                                                        
################## START  Update method ################    


@goal.route('/goal_method_update2/<int:selected_method_id>', methods=['GET', 'POST'])
def goal_method_update2(selected_method_id):

    print("In UUUUUUUUUU 222222222222 goal_method_update2 selected_method_id ", selected_method_id)
    
    method = method_select2(selected_method_id)
    return redirect(url_for('goals.goal_method_update'))			


################## START  Add method ################      
@goal.route('/method_to_goal_add', methods=['GET', 'POST'])
def method_to_goal_add():
    print ("In method_to_goal_add  ")
    
    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a destination first ")
        return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=3))		

    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('destinations.edit_destinations_goals'))		

    form = Todo_form()
    
    form.method_type.choices=[]
    form.who.choices=[]
    form.method_type.choices=[]

    form.who.choices = [(acc.id, acc.title) for acc in Accupation.query.all()]
    form.process()

    form.method_type.choices = [(mt.id, mt.title) for mt in Method_type.query.all()]
    form.process()

    form.due_date = datetime.today()
    form.process()

    first_sts = Status.query.first()

    ### GET Case
    if request.method == 'GET':
        return render_template('method_to_goal_add.html', dst=dst, goal=goal, form=form)
   

    ### POST Case
    ### FROM https://stackoverflow.com/questions/28209131/wtforms-post-with-selectfield-not-working
    print ("form.validate_on_submit", form.validate_on_submit)

    if not form.validate_on_submit:
        flash("יש לבחור קטגוריה")
        return render_template('method_to_goal_add.html', form=form)
        
        
    print ("POST -- In method_to_goal_add -- POST   ")
                       
    author_id = current_user._get_current_object().id  

    method = Method(request.form['title'], request.form['body'], author_id)        
    db.session.add(method)
        
    print("method.children ", goal.children )
    
    ### asign TO  HUMPTY DUMPTY THE NEW TODO
    hd = get_dummy_student()
    std_gt = attach_gt_to_std(hd.id, method.id) 
   
    default_sts = Status.query.filter(Status.default==True).first()    
    method.set_parent(default_sts)    
    std_gt.status_id = default_sts.id
        
    who = Accupation.query.filter(Accupation.id==request.form.get('who')).first()    
    method_type = Method_type.query.filter(Method_type.id==request.form.get('method_type')).first()    
                       
    goal.set_parent(method)
    goal.set_parent(method_type)
    method_type.set_parent(method)
    goal.set_parent(who)
    method.set_parent(who)
    method.set_parent(method_type)
    
            
    db.session.commit()  
    db.session.refresh(method)
    
    ##########import pdb;; pdb.set_trace()


    return redirect(url_for('goals.edit_goal_methods'))		

                                                    
################## START  Add method ################    


@goal.route('/method_to_goal_add2/<int:selected_general_txt_id>', methods=['GET', 'POST'])
def method_to_goal_add2(selected_general_txt_id):
	print(selected_general_txt_id)
	goal = goal_select2(selected_general_txt_id)
	return redirect(url_for('goals.method_to_goal_add'))			

	
@goal.route('/method_from_goal_delete', methods=['GET', 'POST'])
def method_from_goal_delete():
	
    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('select.goal_select'))		

    method = Method.query.filter(Method.selected==True).first()
    if method == None:
        flash("Please select a method to delete first ")
        return redirect(url_for('goals.edit_goal_methods'))
            
    print ("delete selected method is " + method.title + " from slected goal " + goal.title )

    goal.children.remove(method)
    db.session.commit()  

    return redirect(url_for('goals.edit_goal_methods')) 
 
 
@goal.route('/method_from_goal_delete2/<int:selected_goal_id>/<int:selected_method_id>', methods=['GET', 'POST'])
def method_from_goal_delete2(selected_goal_id, selected_method_id):

    print("totdo id: ", selected_method_id)
    method = method_select2(selected_method_id)
      
    goal = goal_select2(selected_goal_id)
              
    return redirect(url_for('goals.method_from_goal_delete')) 	

##############goal's methods ###############	




##############START goal's tests###############	

@goal.route('/edit_goal_tests', methods=['GET', 'POST'])
def edit_goal_tests():

    #####import pdb; pdb.set_trace()
    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a destination first ")
        return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=3))	

    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('destinations.edit_destinations_goals'))	

    std = get_dummy_student()
    print("In edit_goal_tests dummy_std   goal id : ", std.id, goal.id )
    return render_template('./tests/edit_goal_tests.html', dst=dst, goal=goal)                                             
                                                                
														  		
@goal.route('/edit_goal_tests2/<int:selected_goal_id>', methods=['GET', 'POST'])
def edit_goal_tests2(selected_goal_id):
    print("In edit_goal_tests2 Request is :", request)
    goal = goal_select2(selected_goal_id)
    return redirect(url_for('goals.edit_goal_tests'))		


################## START  Update test ################    
@goal.route('/goal_test_update', methods=['GET', 'POST'])
def goal_test_update():

    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a goal first ")
        return redirect(url_for('destinations.edit_destinations_goals'))	
             
    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('destinations.edit_destinations_goals'))	
        
    test = Test.query.filter(Test.selected==True).first()
    if test == None:
        flash("Please select a test first ")
        return redirect(url_for('goals.edit_goal_tests'))		
 
    print ("In  goal_test_update goal: ", dst, goal, test )

    #DEBUG ONLY

    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a destination first ")
        return redirect(url_for('destinations.edit_destinations_goals'))	
    #DEBUG ONLY
   
    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('destinations.edit_destinations_goals'))	
    #DEBUG ONLY
         
    
    form = Todo_form()

    form.title = test.title
    form.body =  test.body
    
         
    ### GET Case
    if request.method == 'GET': 
        return render_template('./tests/update_test.html', form=form, dst=dst, goal=goal)  
        
    ### POST Case
    ### FROM https://stackoverflow.com/questions/28209131/wtforms-post-with-selectfield-not-working
    print ("form.validate_on_submit", form.validate_on_submit)

    if not form.validate_on_submit:
        flash("יש לבחור קטגוריה")
        return render_template('dsply_test_form.html', form=form)
        
    ##################  Fill test fields 
    #########################import pdb;;pdb.set_trace()

    test.title = request.form['title'] 
    test.body =  request.form['body']
        
    goal.set_parent(test)
    
    ##################  Fill test fields   
                
    db.session.commit()  
    db.session.refresh(test)
    
    return redirect(url_for('goals.edit_goal_tests', dst=dst, goal=goal ))   
                                                        
################## START  Update test ################    


@goal.route('/goal_test_update2/<int:selected_test_id>', methods=['GET', 'POST'])
def goal_test_update2(selected_test_id):

    print("In UUUUUUUUUU 222222222222 goal_test_update2 selected_test_id ", selected_test_id)
    
    test = test_select2(selected_test_id)
    return redirect(url_for('goals.goal_test_update'))			


################## START  Add test ################      
@goal.route('/test_to_goal_add', methods=['GET', 'POST'])
def test_to_goal_add():
    print ("In test_to_goal_add  ")
    
    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a destination first ")
        return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=3))		

    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('destinations.edit_destinations_goals'))		

    form = Todo_form()
    
    form.due_date = datetime.today()
    form.process()

    first_sts = Status.query.first()

    ### GET Case
    if request.method == 'GET':
        return render_template('./tests/test_to_goal_add.html', dst=dst, goal=goal, form=form)
   

    ### POST Case
    ### FROM https://stackoverflow.com/questions/28209131/wtforms-post-with-selectfield-not-working
    print ("form.validate_on_submit", form.validate_on_submit)

    if not form.validate_on_submit:
        flash("יש לבחור קטגוריה")
        return render_template('./tests/test_to_goal_add.html', form=form)
        
        
    print ("POST -- In test_to_goal_add -- POST   ")
                       
    author_id = current_user._get_current_object().id  

    test = Test(request.form['title'], request.form['body'], author_id)        
    db.session.add(test)
        
    print("test.children ", goal.children )
    
    ### asign TO  HUMPTY DUMPTY THE NEW TODO
    hd = get_dummy_student()
    std_gt = attach_gt_to_std(hd.id, test.id) 
   
    default_sts = Status.query.filter(Status.default==True).first()    
    test.set_parent(default_sts)    
    std_gt.status_id = default_sts.id
                               
    goal.set_parent(test)
    
            
    db.session.commit()  
    db.session.refresh(test)
    
    ##########import pdb;; pdb.set_trace()


    return redirect(url_for('goals.edit_goal_tests'))		

                                                    
################## START  Add test ################    


@goal.route('/test_to_goal_add2/<int:selected_general_txt_id>', methods=['GET', 'POST'])
def test_to_goal_add2(selected_general_txt_id):
	print(selected_general_txt_id)
	goal = goal_select2(selected_general_txt_id)
	return redirect(url_for('goals.test_to_goal_add'))			

	
@goal.route('/test_from_goal_delete', methods=['GET', 'POST'])
def test_from_goal_delete():
	
    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('select.goal_select'))		

    test = Test.query.filter(Test.selected==True).first()
    if test == None:
        flash("Please select a test to delete first ")
        return redirect(url_for('goals.edit_goal_tests'))
            
    print ("delete selected test is " + test.title + " from slected goal " + goal.title )

    goal.children.remove(test)
    db.session.commit()  

    return redirect(url_for('goals.edit_goal_tests')) 
 
 
@goal.route('/test_from_goal_delete2/<int:selected_goal_id>/<int:selected_test_id>', methods=['GET', 'POST'])
def test_from_goal_delete2(selected_goal_id, selected_test_id):

    print("totdo id: ", selected_test_id)
    test = test_select2(selected_test_id)
      
    goal = goal_select2(selected_goal_id)
              
    return redirect(url_for('goals.test_from_goal_delete')) 	

##############goal's tests ###############	





##############goal's files ###############


@goal.route('/get_goal_files', methods=['GET', 'POST'])
def get_goal_files():

    all_files = Ufile.query.all()   #Reset files selection
    for f in all_files:
        f.selected = False
        
    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a goal first ")
        return redirect(url_for('destinations.edit_destinations',from_dst_sort_order=3 ))	
        
    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('destinations.edit_destinations_goals'))	

    goal_files = []
    for c in goal.children:
        if c.type=='resource':
            if c.ufile_id != None:
                r_file = Ufile.query.filter(Ufile.id==c.ufile_id).first()
                print("")
                print("IN edit_goal_files setting goal_files-- ", r_file, r_file.id)
                print("")
                goal_files.append(r_file)
                
    print("In edit_goal_files student goal goal_files: ", goal, goal_files )
    print("")
    print("")
    return goal_files
          

@goal.route('/edit_goal_files', methods=['GET', 'POST'])
def edit_goal_files():

    all_files = Ufile.query.all()   #Reset files selection
    for f in all_files:
        f.selected = False
        
    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a goal first ")
        return redirect(url_for('destinations.edit_destinations',from_dst_sort_order=3 ))	
        
    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('destinations.edit_destinations_goals'))	

    goal_files = []
    for c in goal.children:
        if c.type=='resource':
            if c.ufile_id != None:
                r_file = Ufile.query.filter(Ufile.id==c.ufile_id).first()
                print("")
                print("IN edit_goal_files setting goal_files-- ", r_file, r_file.id)
                print("")
                goal_files.append(r_file)
                
    print("In edit_goal_files student goal goal_files: ", goal, goal_files )
    print("")
    return render_template('edit_goal_files.html', dst=dst, goal=goal, goal_files=goal_files) 
                                                                
														  		
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
    
    ###########import pdb; pdb.set_trace()

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
    ########import pdb; pdb.set_trace()
    
    downloaded_file =  send_file(BytesIO(downloaded_file.data), attachment_filename=downloaded_file.name, as_attachment=True)
    return downloaded_file
 
        
@goal.route('/download_goal_file2/<int:selected_file_id>', methods=['GET', 'POST'])
def download_goal_file2(selected_file_id):
    ########import pdb; pdb.set_trace()
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

    ########import pdb; pdb.set_trace()
    
    author_id = current_user._get_current_object().id

    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('goals.edit_goal_files'))	
            
    #######import pdb; pdb.set_trace()
    
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
    
    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a destination first ")
        return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=3))		
    
    goal = goal_select2(selected_goal_id)
    
    if request.method == 'GET':
        return render_template('upload_new_file.html', dst=dst, goal=goal)

    uploaded_file = request.files.get('file_name')  # probably can be done only in post upload_new_file2
    
    print("")
    print("")
    print("IN goals: UPLOADED-FILE-NAME --- request.files.get('file_name')", uploaded_file)
    print("")
    
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
