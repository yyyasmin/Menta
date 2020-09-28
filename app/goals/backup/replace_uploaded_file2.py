    
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

