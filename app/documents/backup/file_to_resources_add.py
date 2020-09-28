	
@resource.route('/file_to_resource_add', methods=['GET', 'POST'])
def file_to_resource_add():
    author_id = current_user._get_current_object().id

    resource = Resource.query.filter(Resource.selected==True).first()
    if resource == None:
        flash("Please select a resource first ")
        return redirect(url_for('select.resource_select'))		

    if request.method == 'GET':
        return render_template('file_to_resource_add.html', resource=resource)
           
    #get data from form and insert to filegress db
    title = request.form.get('title')
    body = request.form.get('description')

    file_name = request.form.get('file_name')
    uploaded_file = request.files.get('file_name')
    file_name = uploaded_file.filename
    file_data = uploaded_file.read()
    uploaded_file = Ufile(file_name, file_data, author_id)  #find out how to set file_data

    ##import pdb; pdb.set_trace() 	


    db.session.add(uploaded_file)    	
    resource.files.append(uploaded_file)   
    db.session.commit()  
    db.session.refresh(file)
    return redirect(url_for('resources.edit_resource_uploaded_files'))	

@resource.route('/file_to_resource_add2/<int:selected_resource_id>', methods=['GET', 'POST'])
def file_to_resource_add2(selected_resource_id):
	print(selected_resource_id)
	resource = resource_select2(selected_resource_id)
	return redirect(url_for('resources.file_to_resource_add'))			
