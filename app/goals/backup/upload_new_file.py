	
@goal.route('/upload_new_file', methods=['GET', 'POST'])
def upload_new_file():
    
    author_id = current_user._get_current_object().id

    goal = Goal.query.filter(Goal.selected==True).first()
    if goal == None:
        flash("Please select a goal first ")
        return redirect(url_for('select.goal_select'))	

      
    print("Request is: ", request)
    if request.method == 'GET':
        return render_template('goal_upload_file.html', goal=goal)
               
    #Can be done only in post function2 ???
    import pdb; pdb.set_trace()
    title = request.form.get('title')  # probably can be done only in post upload_new_file2
    body = request.form.get('description')  # probably can be done only in post upload_new_file2

    uploaded_file = request.files.get('file_name')  # probably can be done only in post upload_new_file2
    ###import pdb; pdb.set_trace()
    file_name = uploaded_file.filename
    file_data = uploaded_file.read()

    uploaded_file = Ufile.query.filter(uploaded_file.name == file_name).first()
    if uploaded_file == None:
        uploaded_file = Ufile(file_name, file_data, author_id)  #find out how to set file_data
        db.session.add(uploaded_file)
        db.session.commit()

    # Match the new file to a  (created if does'nt exist) resource
    resource = Resource.query.filter(Resource.ufile_id==uploaded_file.id).first()
    if resource == None:
        new_resource = Resource(file_name, file_data, author_id) 
        db.session.add(new_resource)
        db.session.commit()

    new_resource.ufile_id = uploaded_file.id 
    goal.set_parent(new_resource)
    
    db.session.commit()  
        
    print("Uloading a new file to goal: ", goal, .goal.id)
    print("goal_upload_new_file uploaded file is: ", uploaded_file, uploaded_file.id)
    
    url = url_for('goals.edit_goal_files' )
    return redirect(url)   

@goal.route('/upload_new_file2/<int:selected_goal_id>', methods=['GET', 'POST'])
def upload_new_file2(selected_goal_id):
	print("in goal_upload_new_file2 selected_goal_id is: ", selected_goal_id)
	goal = goal_select2(selected_goal_id)
	return redirect(url_for('goals.upload_new_file'))		
    
