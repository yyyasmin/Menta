

##############goal's resources###############	

@goal.route('/edit_goal_files', methods=['GET', 'POST'])
def edit_goal_files():

	goal = Goal.query.filter(Goal.selected==True).first()
	if goal == None:
		flash("Please select a goal first ")
		return redirect(url_for('destinations.edit_destination_goals'))	
    
    goal_files = []
    for c in goal.children.all():
        if c.type=='resource':
            r_file = Ufile.query.filter(Ufile.id==c.ufile_id).first()
            goal_files.append(c)
            
	print("In edit_goal_resources student for show tree: " )
	return render_template('edit_goal_files.html', goal=goal, goal_files=goal_files) 
																
														  		
@goal.route('/edit_goal_files/<int:selected_file_id>', methods=['GET', 'POST'])
def edit_goal_files(selected_goal_id):
	print("In edit_goal_resources2 Request is :", request)
	file = file_select2(selected_goal_id)
	return redirect(url_for('goals.edit_goal_files'))		

	
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
