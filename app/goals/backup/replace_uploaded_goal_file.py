
	
@rsrc.route('/uploaded_file_from_goal_delete', methods=['GET', 'POST'])
def uploaded_file_from_goal_delete():

    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('select.edit_destination_goals'))	

    uploaded_file = Ufile.query.filter(Ufile.selected==True).first()
    if uploaded_file == None:
        flash("Please select a uploaded_file to delete first ")
        return url_for('resources.edit_goal_files')

    #import pdb; pdb.set_trace()
    
    resource = Resource.query.filter(Resource.ufile_id==uploaded_file.id).first()
    if resource == None:
        flash("Please select a resource first ")
        return redirect(url_for('select.resource_select'))		
    
    goal.unset_parent(resource)
    
    #import pdb; pdb.set_trace()
    db.session.commit()  

    return redirect(url_for('resources.edit_goal_files')) 

@rsrc.route('/uploaded_file_from_goal_delete2/<int:selected_file_id>', methods=['GET', 'POST'])
def uploaded_file_from_goal_delete2(selected_file_id):
    
    uploaded_file = file_select2(selected_file_id)
    return uploaded_file_from_resource_delete() 	
	

*********************************************************
	
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

    resource = Resource(title, body, author_id)

    file_name = request.form.get('file_name')
    uploaded_file = request.files.get('file_name')
    file_name = uploaded_file.filename
    file_data = uploaded_file.read()
    uploaded_file = Ufile(file_name, file_data, author_id)  #find out how to set file_data

    #######################import pdb;;pdb.set_trace() 	

    resource.ufile_id = uploaded_file.id
    db.session.add(resource)    	
    goal.set_parent(resource)
    
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

    goal.unset_parent(resource)
    db.session.commit()  

    return redirect(url_for('goals.edit_goal_resources')) 

@goal.route('/resource_from_goal_delete2/<int:selected_goal_id>/<int:selected_resource_id>', methods=['GET', 'POST'])
#Here author is user_id
def resource_from_goal_delete2(selected_goal_id, selected_resource_id):
    goal = goal_select2(selected_goal_id)

    resource = resource_select2(selected_resource_id)
    
    return redirect(url_for('goals.resource_from_goal_delete')) 	

############## END goal's resources###############	




********************************


##############resource's download_files###############	

    
@goal.route('/replace_uploaded_file', methods=['GET', 'POST'])
def replace_uploaded_file():
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

@goal.route('/replace_uploaded_file2/<int:selected_file_id>', methods=['GET', 'POST'])
def replace_uploaded_file2(selected_file_id):
	print("in resource_upload_file2 selected_file_id is: ", selected_file_id)
	file = file_select2(selected_file_id)
	return redirect(url_for('resources.resource_upload_new_file'))	

    
@goal.route('/replace_uploaded_file', methods=['GET', 'POST'])
def replace_uploaded_file():
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

@goal.route('/replace_uploaded_file2/<int:selected_file_id>', methods=['GET', 'POST'])
def replace_uploaded_file2(selected_file_id):
	print("in resource_upload_file2 selected_file_id is: ", selected_file_id)
	file = file_select2(selected_file_id)
	return redirect(url_for('resources.resource_upload_new_file'))	


**********************************