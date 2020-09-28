from io import BytesIO

	
@rsrc.route('/download_resource_file', methods=['GET', 'POST'])
def download_resource_file():
    author_id = current_user._get_current_object().id

    resource = Resource.query.filter(Resource.selected==True).first()
    if resource == None:
        flash("Please select a resource first ")
        return redirect(url_for('select.resource_select'))	
    
    downloaded_file = Ufile.query.filter(Ufile.selected==True).first() 
    if downloaded_file == None:
        flash("Please select a resource first ")
        return redirect(url_for('select.file_select'))	

    downloaded_file =  send_file(BytesIO(downloaded_file.data, attachment_file=downloaded_file.filename, as_attachment=True)
    print("Downloaded file: ", downloaded_file)
    return render_template('edit_resource_uploaded_files.html', resource=resource) 
 
    
    
@rsrc.route('/download_resource_file2/<int:selected_resource_id>/<int:selected_download_file_id>', methods=['GET', 'POST'])
def download_resource_file2(selected_resource_id, selected_download_file_id):
	print(selected_resource_id)
	resource = resource_select2(selected_resource_id)
    downloded_file = file_select2(selected_download_file_id)

	return redirect(url_for('resources.download_resource_file'))			

