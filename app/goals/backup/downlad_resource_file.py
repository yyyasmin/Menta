
	
##############resource's download_files###############	

from io import BytesIO
from flask.helpers import send_file
	
@rsrc.route('/download_resource_file', methods=['GET', 'POST'])
def download_resource_file():

    print("HHHHHHHHHHHHere in download_resource_file")
    
    author_id = current_user._get_current_object().id
    
    ##import pdb; pdb.set_trace()

    resource = Resource.query.filter(Resource.selected==True).first()
    if resource == None:
        flash("Please select a resource first ")
        return redirect(url_for('select.resource_select'))	

    downloaded_file = Ufile.query.filter(Ufile.selected==True).first() 
    if downloaded_file == None:
        flash("Please select a resource first ")
        return redirect(url_for('select.file_select'))	

    ##import pdb; pdb.set_trace()
    
    downloaded_file =  send_file(BytesIO(downloaded_file.data), attachment_filename=downloaded_file.name, as_attachment=True)
    return downloaded_file
    #print("Downloaded file: ", downloaded_file)
    #return render_template('edit_resource_uploaded_files.html', resource=resource) 
 
    
    
@rsrc.route('/download_resource_file2/<int:selected_file_id>', methods=['GET', 'POST'])
def download_resource_file2(selected_file_id):
    downloded_file = file_select2(selected_file_id)
    ##import pdb; pdb.set_trace()
    return download_resource_file()			

##############resource's download_files###############	
