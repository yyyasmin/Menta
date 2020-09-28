from flask import render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy

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

from sqlalchemy import update

from app.content_management import Content

#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
from flask import Blueprint
rsrc = Blueprint(
    'resources', __name__,
    template_folder='templates'
)   
#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
from app.select.select import profile_select2, strength_select2, destination_select2, goal_select2, resource_select2, file_select2

from app import *


################### resources ####################

#update selected resource
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@rsrc.route('/resource_update/<int:selected_resource_id>', methods=['GET', 'POST'])
def resource_update(selected_resource_id):

    ####import pdb; pdb.set_trace()
    
    author_id = current_user._get_current_object().id
    
    destination = Destination.query.filter(Destination.selected==True).first()
    if destination == None:
        flash("Please select a destination first ")
        return redirect(url_for('index'))
        
    goal = Goal.query.filter(Goal.selected==True).first()
    print(" In resource_update goal selected is")
    print(goal.title)
    
    if goal == None:
        flash("Please select an goal first ")
        return redirect(url_for('goal_select'))
    print(goal.title)      
    #print request
    
    resource_select2(selected_resource_id)	
    resource = Resource.query.get_or_404(selected_resource_id)
	
    if request.method == 'GET':
        return render_template('update_resource.html', goal=goal, resource=resource)
		
    #get data from form and insert to destinationgress db
    #######import pdb; pdb.set_trace() 	
    resource.title = request.form.get('title')
    resource.body = request.form.get('description')
    
    db.session.commit()  
    db.session.refresh(resource)
	
    return redirect(url_for('goals.edit_goal_resources'))		
#end update selected resource 		
	
@rsrc.route('/resources/add', methods=['GET', 'POST'])
def resources_add():

    author_id = current_user._get_current_object().id

    dst = Destination.query.filter(Destination.selected==True).first()
    if dst == None:
        flash("Please select a destination first ")
        return redirect(url_for('destinations.edit_destinations', from_dst_sort_order=0))		

    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('select.edit_destination_goals'))	

    if request.method == 'GET':
        return render_template('add_resources.html', goal=goal)
       
    #get data from form and insert to destinationgress db
    body = request.form.get('description')

    #######import pdb; pdb.set_trace() 	
    resource = Resource(body)	

    goal.resources.append(resource)	

    db.session.add(resource)    
    db.session.commit()  
    db.session.refresh(resource)
    # test insert res
    return redirect(url_for('goals.edit_goal_resources'))		

@rsrc.route('/resources/add/<int:selected_goal_id>', methods=['GET', 'POST'])
def resources_add2(selected_goal_id):
    goal_select2(selected_goal_id)
    return redirect(url_for('resources_add'))


@rsrc.route('/resource/delete/', methods=['GET', 'POST'])
#Here author is user_id
def resource_delete():  
    destination = Destination.query.filter(Destination.selected==True).first()
    print(destination.title)
    if destination == None:
        flash("Please select a destination first ")
        return redirect(url_for('destination_select'))
		
    resource = Resource.query.filter(Resource.selected==True).first()
    
    if resource == None:
        flash("Please select a resource to delete first ")
        return redirect(url_for('resource_select'))

    print("deleteint resource %s ", resource.description)		
    db.session.delete(resource)		
    db.session.commit()  
	
    return redirect(url_for('resources.resources_by_goal'))
#end goal_delete
		
#goal_delete2
@rsrc.route('/resource/delete2/<int:selected_resource_id>', methods=['GET', 'POST'])
def resource_delete2(selected_resource_id):
    resource_select2(selected_resource_id)
    return redirect(url_for('resource_delete'))
#end goal_delete2
################### resources ####################



##############resource's uploaded_files###############	


#update selected file
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@rsrc.route('/file/update/<int:selected_file_id>', methods=['GET', 'POST'])
def file_update(selected_file_id):
    
    ####import pdb; pdb.set_trace()
    
    author_id = current_user._get_current_object().id
    
    destination = Destination.query.filter(Destination.selected==True).first()
    if destination == None:
        flash("Please select a destination first ")
        return redirect(url_for('index'))
        
    goal = Goal.query.filter(Goal.selected==True).first()
    print(" In file_update goal selected is")
    print(goal.title)
    
    if goal == None:
        flash("Please select an goal first ")
        return redirect(url_for('goal_select'))
    print(goal.title)      
    #print request
    
    file_select2(selected_file_id)	
    file = Ufile.query.get_or_404(selected_file_id)
	
    if request.method == 'GET':
        return render_template('update_file.html', goal=goal, file=file)
		
    #get data from form and insert to destinationgress db
    #######import pdb; pdb.set_trace() 	
    file.title = request.form.get('title')
    file.body = request.form.get('description')
    file.selected=False
    db.session.commit()  
    db.session.refresh(file)
	
    return redirect(url_for('resources.edit_resource_uploaded_files'))		
#end update selected file 	

@rsrc.route('/edit_resource_uploaded_files', methods=['GET', 'POST'])
def edit_resource_uploaded_files():

	resource = Resource.query.filter(Resource.selected==True).first()
	if resource == None:
		flash("Please select a resource first ")
		return redirect(url_for('select.resource_select'))		
	print("In edit_resource_uploaded_files  resources aer:  ", resource )
	return render_template('edit_resource_files.html', resource=resource) 
																														  		
@rsrc.route('/edit_resource_uploaded_files2/<int:selected_resource_id>', methods=['GET', 'POST'])
def edit_resource_uploaded_files2(selected_resource_id):
	print("In edit_resource_uploaded_files2 selected_resource_id is :", selected_resource_id)
	rsrc = resource_select2(selected_resource_id)
	return redirect(url_for('resources.edit_resource_uploaded_files'))		

	
@rsrc.route('/resource_upload_new_file', methods=['GET', 'POST'])
def resource_upload_new_file():
    
    author_id = current_user._get_current_object().id

    resource = Resource.query.filter(Resource.selected==True).first()
    if resource == None:
        flash("Please select a resource first ")
        return redirect(url_for('select.resource_select'))	
        
    print("Request is: ", request)
    if request.method == 'GET':
        return render_template('resource_upload_file.html', resource=resource)
               
    #get data from form and insert to uploaded_filegress db
    title = request.form.get('title')
    body = request.form.get('description')

    uploaded_file = request.files.get('file_name')
    ###import pdb; pdb.set_trace()
    file_name = uploaded_file.filename
    file_data = uploaded_file.read()

    uploaded_file = Ufile.query.filter(uploaded_file.name == file_name).first()
    if uploaded_file == None:
        uploaded_file = Ufile(file_name, file_data, author_id)  #find out how to set file_data
        db.session.add(uploaded_file)
        db.session.commit()
        
    resource.ufile_id = uploaded_file.id    
    db.session.commit()  
        
    print("resource_upload_new_file uploaded file is: ", uploaded_file)
    
    url = url_for('resources.edit_resource_uploaded_files' )
    return redirect(url)   

@rsrc.route('/resource_upload_new_file2/<int:selected_resource_id>', methods=['GET', 'POST'])
def resource_upload_new_file2(selected_resource_id):
	print("in resource_upload_new_file2 selected_resource_id is: ", selected_resource_id)
	resource = resource_select2(selected_resource_id)
	return redirect(url_for('resources.resource_upload_new_file'))		
    
    
@rsrc.route('/resource_replace_upload_file', methods=['GET', 'POST'])
def resource_replace_upload_file():
    author_id = current_user._get_current_object().id

    resource = Resource.query.filter(Resource.selected==True).first()
    if resource == None:
        flash("Please select a resource first ")
        return redirect(url_for('select.resource_select'))	
        
    uploaded_file = Ufile.query.filter(Ufile.selected==True).first()
    if uploaded_file == None:
        flash("Please select a file to update ")
        return redirect(url_for('resources.edit_resource_uploaded_files'))	
        
    redirect(url_for('resources.uploaded_file_from_resource_delete'))
    redirect(url_for('resources.resource_upload_new_file'))

    db.session.commit()
    
    url = url_for('resources.edit_resource_uploaded_files' )
    return redirect(url)   

@rsrc.route('/resource_replace_upload_file2/<int:selected_file_id>', methods=['GET', 'POST'])
def resource_replace_upload_file2(selected_file_id):
	print("in resource_upload_file2 selected_file_id is: ", selected_file_id)
	file = file_select2(selected_file_id)
	return redirect(url_for('resources.resource_upload_new_file'))	

	
@rsrc.route('/uploaded_file_from_resource_delete', methods=['GET', 'POST'])
def uploaded_file_from_resource_delete():

    resource = Resource.query.filter(Resource.selected==True).first()
    if resource == None:
        flash("Please select a resource first ")
        return redirect(url_for('select.resource_select'))		


    uploaded_file = Ufile.query.filter(Ufile.selected==True).first()
    if uploaded_file == None:
        flash("Please select a uploaded_file to delete first ")
        return url_for('resources.edit_resource_uploaded_files' )

    #import pdb; pdb.set_trace()
    print ("delete selected uploaded_file is " + uploaded_file.name + " from slected resource " + resource.title )

    
    #import pdb; pdb.set_trace()
    db.session.commit()  

    return redirect(url_for('resources.edit_resource_uploaded_files')) 

@rsrc.route('/uploaded_file_from_resource_delete2/<int:selected_file_id>', methods=['GET', 'POST'])
def uploaded_file_from_resource_delete2(selected_file_id):
    
    uploaded_file = file_select2(selected_file_id)
    return uploaded_file_from_resource_delete() 	

##############resource's uploaded_files###############

	
##############resource's download_files###############	

from io import BytesIO
from flask.helpers import send_file
	
@rsrc.route('/download_resource_file', methods=['GET', 'POST'])
def download_resource_file():

    print("HHHHHHHHHHHHere in download_resource_file")
    
    author_id = current_user._get_current_object().id
    
    ##import pdb; pdb.set_trace()

    resource = Resource.query.filter(Resource.selected==True).first()
    if resource == None:
        flash("Please select a resource first ")
        return redirect(url_for('select.resource_select'))	

    downloaded_file = Ufile.query.filter(Ufile.selected==True).first() 
    if downloaded_file == None:
        flash("Please select a resource first ")
        return redirect(url_for('select.file_select'))	

    ##import pdb; pdb.set_trace()
    
    downloaded_file =  send_file(BytesIO(downloaded_file.data), attachment_filename=downloaded_file.name, as_attachment=True)
    return downloaded_file
    #print("Downloaded file: ", downloaded_file)
    #return render_template('edit_resource_uploaded_files.html', resource=resource) 
 
    
    
@rsrc.route('/download_resource_file2/<int:selected_file_id>', methods=['GET', 'POST'])
def download_resource_file2(selected_file_id):
    downloded_file = file_select2(selected_file_id)
    ##import pdb; pdb.set_trace()
    return download_resource_file()			

##############resource's download_files###############	

	
		
