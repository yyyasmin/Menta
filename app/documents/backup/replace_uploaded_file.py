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
    file_name = uploaded_file.filename
    file_data = uploaded_file.read()
    uploaded_file = Ufile(file_name, file_data, author_id)  #find out how to set file_data

    ###import pdb; pdb.set_trace() 	
    resource.files.append(uploaded_file)
    '''
    tag = Tag.query.filter(Tag.title==tag_title).first()	
    if tag == None:	    	     
        tag = Tag(tag_title)	
        print(tag.title)				
        db.session.add(tag)
        
    uploaded_file.tags.append(tag)
    ''' 
    ##import pdb; pdb.set_trace()
    db.session.add(uploaded_file)    	
    resource.files.append(uploaded_file)   
    db.session.commit()  
    
    db.session.refresh(uploaded_file)
    db.session.refresh(resource)

    url = url_for('resources.edit_resource_uploaded_files' )
    return redirect(url)   

@rsrc.route('/resource_upload_new_file2/<int:selected_resource_id>', methods=['GET', 'POST'])
def resource_upload_new_file2(selected_resource_id):
	print(selected_resource_id)
	resource = resource_select2(selected_resource_id)
	return redirect(url_for('resources.resource_upload_new_file'))		
    
    
@rsrc.route('/resource_replace_upload_file', methods=['GET', 'POST'])
def resource_replace_upload_file():
    author_id = current_user._get_current_object().id

    resource = Resource.query.filter(Resource.selected==True).first()
    if resource == None:
        flash("Please select a resource first ")
        return redirect(url_for('select.resource_select'))	
        

    uploaded_file = Resource.query.filter(Ufile.selected==True).first()
    if uploaded_file == None:
        flash("Please select a file to update ")
        return redirect(url_for('resources.files_by_resource'))	
        
    redirect(url_for('resources.uploaded_file_from_resource_delete'))
    redirect(url_for('resources.resource_upload_new_file'))

    db.session.commit()      
    db.session.refresh(uploaded_file)
    db.session.refresh(resource)

    url = url_for('resources.edit_resource_uploaded_files' )
    return redirect(url)   

@rsrc.route('/resource_replace_upload_file2/<int:selected_file_id>', methods=['GET', 'POST'])
def resource_replace_upload_file2(selected_file_id):
	print("in resource_upload_file2 selected_file_id is: ", selected_file_id)
	file = file_select2(selected_file_id)
	return redirect(url_for('resources.resource_upload_file'))		