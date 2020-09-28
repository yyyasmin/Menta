    
    
@rsrc.route('/replace_uploaded_file', methods=['GET', 'POST'])
def replace_uploaded_file():
   
    redirect(url_for('resources.uploaded_file_from_goal_delete'))
    redirect(url_for('resources.upload_new_file'))

    db.session.commit()
    
    url = url_for('resources.edit_goal_files' )
    return redirect(url)   

@rsrc.route('/replace_uploaded_file2/<int:selected_file_id>', methods=['GET', 'POST'])
def replace_uploaded_file2(selected_file_id):
	print("in resource_upload_file2 selected_file_id is: ", selected_file_id)
	file = file_select2(selected_file_id)
	return redirect(url_for('resources.resource_upload_new_file'))	

