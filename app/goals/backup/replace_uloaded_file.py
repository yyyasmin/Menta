	
@goal.route('/replace_uploaded_file', methods=['GET', 'POST'])
def replace_uploaded_file():

    #import pdb; pdb.set_trace()
    
    author_id = current_user._get_current_object().id

    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('goals.edit_goal_files'))	
            
    import pdb; pdb.set_trace()
    
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
        
        resource = Resource(file_name, file_data, author_id) 
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


@goal.route('/replace_uploaded_file2/<int:selected_replaced_file_id>', methods=['GET', 'POST'])
def replace_uploaded_file2(selected_replaced_file_id):

    print("in goal_upload_new_file2 selected_replaced_file_id is: ", selected_replaced_file_id)
    
    author_id = current_user._get_current_object().id

    replaced_file = Ufile.query.filter(Ufile.id==selected_replaced_file_id).first()

    import pdb; pdb.set_trace()
    print("")
    print("request.method ": , request.method )
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
    uploaded_new_file = request.files.get('file_name')  # Can be done only here scince it has to be in a post request
    file_name = uploaded_new_file.filename
    file_data = uploaded_new_file.read()

    uploaded_new_file = Ufile.query.filter(uploaded_new_file.name == file_name).first()
    if uploaded_new_file == None:
        uploaded_new_file = Ufile(file_name, file_data, author_id)  #find out how to set file_data
        db.session.add(uploaded_new_file)
        db.session.commit()
        print("")
        print("")
        print(" in upload_new_file2 new file id: ", uploaded_new_file.id)
      
    # Match the new uploaded file to a  (created if does'nt exist) resource
    resource = Resource.query.filter(Resource.ufile_id==uploaded_new_file.id).first()
    if resource == None:
        file_name = uploaded_new_file.name
        file_data = "The Data is in Ufile"        
        resource = Resource(file_name, file_data, author_id) 
        db.session.add(resource)
        db.session.commit()

    resource.ufile_id = uploaded_new_file.id 
    goal.set_parent(resource)

    db.session.commit()  

    print("")    
    print("Uloading a new file to goal: ", goal, goal.id)
    print("goal_upload_new_file uploaded file is: ", uploaded_file, uploaded_file.id)
    print("")
    print("")
    return redirect(url_for('goals.edit_goal_files'))	

    

        
**********************************
    print("in goal_upload_new_file2 selected_goal_id is: ", selected_file_id)
    
    author_id = current_user._get_current_object().id
    
    replaced_file = file_select2(selected_file_id)
    import pdb; pdb.set_trace()
    
    if request.method == 'GET':
        return render_template('replace_uploaded_file.html', replaced_file=replaced_file)

    #remove replaced file    
    resource = Resource.query.filter(Resource.ufile_id==replaced_file.id).first()
    if resource == None:
        flash("Please select a resource first ")
        return redirect(url_for('goals.edit_goal_files'))		
    
    goal.unset_parent(resource)    
    db.session.commit() 
    
    # Uplaod new file
    uploaded_file = request.files.get('file_name')  # Can be done only here scince it has to be in a post request
    file_name = uploaded_file.filename
    file_data = uploaded_file.read()

    uploaded_new_file = Ufile.query.filter(uploaded_file.name == file_name).first()
    if uploaded_new_file == None:
        uploaded_file = Ufile(file_name, file_data, author_id)  #find out how to set file_data
        db.session.add(uploaded_file)
        db.session.commit()
        print("")
        print("")
        print(" in upload_new_file2 new file id: ", uploaded_file.id)
    
    uploaded_file = file_select2(uploaded_file.id)
    return redirect(url_for('goals.upload_new_file' ))
        

		
**********************************************************