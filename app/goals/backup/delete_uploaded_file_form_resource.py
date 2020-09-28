	
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
