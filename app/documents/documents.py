from flask import render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from flask import render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from flask import render_template, flash, redirect, session, url_for, request, jsonify, json
from flask_login import login_user, logout_user, current_user, login_required
#from flask_login import login_manager

from flask_login import LoginManager
from config import basedir
import config

from app import current_app, db
from app.forms import LoginForm

from app.models import User, School, Student, Teacher
from app.models import Profile, Strength, Weakness, Subject
from app.models import Destination, Goal, Todo
from app.models import Resource, Document, Ufile
from app.models import Accupation, Status, Scrt, Tag
from app.models import General_txt, Std_general_txt

from app.forms import LoginForm, EditForm

from sqlalchemy import update

from app.content_management import Content

#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
from flask import Blueprint
doc = Blueprint(
    'documents', __name__,
    template_folder='templates'
)   
#FROM https://github.com/realpython/discover-flask/blob/master/project/users/views.py
from app.select.select import profile_select2, strength_select2, destination_select2, goal_select2, document_select2, file_select2

from app import *


################### documents ####################

#update selected document
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@doc.route('/document_update/<int:selected_document_id>', methods=['GET', 'POST'])
def document_update(selected_document_id):

    ####import pdb; pdb.set_trace()
    
    author_id = current_user._get_current_object().id

    doc = document_select2(selected_document_id)	
	
    if request.method == 'GET':
        return render_template('update_document.html', doc=doc)
		
    #get data from form and insert to destinationgress db
    #######import pdb; pdb.set_trace() 	
    doc.title = request.form.get('title')
    doc.body = request.form.get('description')
    
    db.session.commit()  
    db.session.refresh(document)
	
    return redirect(url_for('students.edit_std_documents'))		
#end update selected document 		
	
@doc.route('/document/add', methods=['GET', 'POST'])
def document_add():

    author_id = current_user._get_current_object().id

    if request.method == 'GET':
        return render_template('add_document.html')
       
    #get data from form and insert to destinationgress db
    body = request.form.get('description')
    title = request.form.get('title')

    #######import pdb; pdb.set_trace() 	
    doc = Document(title, body)	

    db.session.add(doc)    
    db.session.commit()  
    db.session.refresh(doc)
    # test insert res
    return redirect(url_for('students.edit_student_documents'))		

@doc.route('/document/add/<int:selected_goal_id>', methods=['GET', 'POST'])
def document_add2(selected_goal_id):
    goal_select2(selected_goal_id)
    return redirect(url_for('document_add'))


@doc.route('/document/delete/', methods=['GET', 'POST'])
#Here author is user_id
def document_delete():  

    doc = Document.query.filter(Document.selected==True).first()
    
    if doc == None:
        flash("Please select a document to delete first ")
        return redirect(url_for('students.edit_student_documents'))		

    print("deleteint document %s ", doc.title)		
    db.session.delete(doc)		
    db.session.commit()  
	
    return redirect(url_for('students.edit_student_documents'))
#end goal_delete
		
#goal_delete2
@doc.route('/document/delete2/<int:selected_document_id>', methods=['GET', 'POST'])
def document_delete2(selected_document_id):
    doc = document_select2(selected_document_id)
    return redirect(url_for('document_delete'))
################### documents ####################



##############document's uploaded_files###############	


#update selected file
#from https://teamtreehouse.com/community/add-a-a-with-an-href-attribute-that-points-to-the-url-for-the-cancelorder-view-cant-find-my-error 
@doc.route('/file/update/<int:selected_file_id>', methods=['GET', 'POST'])
def file_update(selected_file_id):
    
    ####import pdb; pdb.set_trace()
    
    author_id = current_user._get_current_object().id

    file_select2(selected_file_id)	
    file = Ufile.query.get_or_404(selected_file_id)
	
    if request.method == 'GET':
        return render_template('update_file.html')
		
    #get data from form and insert to destinationgress db
    #######import pdb; pdb.set_trace() 	
    file.title = request.form.get('title')
    file.body = request.form.get('description')
    file.selected=False
    db.session.commit()  
    db.session.refresh(file)
	
    return redirect(url_for('documents.edit_document_uploaded_files'))		
#end update selected file 	

@doc.route('/edit_document_uploaded_files', methods=['GET', 'POST'])
def edit_document_uploaded_files():

	doc = Document.query.filter(Document.selected==True).first()
	if doc == None:
		flash("Please select a document first ")
		return redirect(url_for('select.document_select'))		
	print("In edit_document_uploaded_files  documents aer:  ", doc )
	return render_template('edit_doc_files.html', doc=doc) 
																														  		
@doc.route('/edit_document_uploaded_files2/<int:selected_document_id>', methods=['GET', 'POST'])
def edit_document_uploaded_files2(selected_document_id):
	print("In edit_document_uploaded_files2 selected_document_id is :", selected_document_id)
	doc = document_select2(selected_document_id)
	return redirect(url_for('documents.edit_document_uploaded_files'))		

	
@doc.route('/document_upload_new_file', methods=['GET', 'POST'])
def document_upload_new_file():

    author_id = current_user._get_current_object().id

    doc = Document.query.filter(Document.selected==True).first()
    if doc == None:
        flash("Please select a document first ")
        return redirect(url_for('select.document_select'))	
        
    print("Request is: ", request)
    if request.method == 'GET':
        return render_template('document_upload_file.html', doc=doc)
         
    #get data from form and insert to uploaded_filegress db
    title = request.form.get('title')
    body = request.form.get('description')

    uploaded_file = request.files.get('file_name')
    ###import pdb; pdb.set_trace()
    file_name = uploaded_file.filename
    file_data = uploaded_file.read()
    uploaded_file = Ufile(file_name, file_data, author_id)  #find out how to set file_data

    new_file = Ufile.query.filter(uploaded_file.name == file_name).first()
    if new_file == None:
        db.session.add(uploaded_file)
    
    if uploaded_file not in doc.files:
        doc.files.append(uploaded_file) 
            
    db.session.commit()  
    
    db.session.refresh(uploaded_file)
    
    print("document_upload_new_file uploaded file is: ", uploaded_file)
    
    db.session.refresh(doc)

    url = url_for('documents.edit_document_uploaded_files' )
    return redirect(url)   

@doc.route('/document_upload_new_file2/<int:selected_document_id>', methods=['GET', 'POST'])
def document_upload_new_file2(selected_document_id):
	print("in document_upload_new_file2 selected_document_id is: ", selected_document_id)
	document = document_select2(selected_document_id)
	return redirect(url_for('documents.document_upload_new_file'))		
    
    
@doc.route('/document_replace_upload_file', methods=['GET', 'POST'])
def document_replace_upload_file():
    author_id = current_user._get_current_object().id

    doc = Document.query.filter(Document.selected==True).first()
    if doc == None:
        flash("Please select a document first ")
        return redirect(url_for('students.edit_student_documents'))	
        

    uploaded_file = Ufile.query.filter(Ufile.selected==True).first()
    if uploaded_file == None:
        flash("Please select a file to update ")
        return redirect(url_for('documents.edit_document_uploaded_files'))	

    db.session.commit()      
    db.session.refresh(uploaded_file)
    db.session.refresh(document)

    return redirect(url_for('documents.edit_document_uploaded_files' ))   

@doc.route('/document_replace_upload_file2/<int:selected_file_id>', methods=['GET', 'POST'])
def document_replace_upload_file2(selected_file_id):
	print("in document_upload_file2 selected_file_id is: ", selected_file_id)
	file = file_select2(selected_file_id)
	return redirect(url_for('documents.document_upload_new_file'))	

	
@doc.route('/uploaded_file_from_document_delete', methods=['GET', 'POST'])
def uploaded_file_from_document_delete():

    doc = Document.query.filter(Document.selected==True).first()
    if doc == None:
        flash("Please select a document first ")
        return redirect(url_for('students.edit_student_documents'))	


    uploaded_file = Ufile.query.filter(Ufile.selected==True).first()
    if uploaded_file == None:
        flash("Please select a uploaded_file to delete first ")
        return url_for('documents.edit_document_uploaded_files' )

    #import pdb; pdb.set_trace()
    print ("delete selected uploaded_file is " + uploaded_file.name + " from slected document " + doc.title )

    for i in range(0, 5):
        document.files.remove(doc.files[i])
        db.session.commit() 

    #import pdb; pdb.set_trace()
    db.session.commit()  

    return redirect(url_for('documents.edit_document_uploaded_files')) 

@doc.route('/uploaded_file_from_document_delete2/<int:selected_file_id>', methods=['GET', 'POST'])
def uploaded_file_from_document_delete2(selected_file_id):
    
    uploaded_file = file_select2(selected_file_id)
    return uploaded_file_from_document_delete() 	

##############document's uploaded_files###############

	
##############document's download_files###############	

from io import BytesIO
from flask.helpers import send_file
	
@doc.route('/download_document_file', methods=['GET', 'POST'])
def download_document_file():

    print("HHHHHHHHHHHHere in download_document_file")
    
    author_id = current_user._get_current_object().id
    
    ##import pdb; pdb.set_trace()

    doc = Document.query.filter(Document.selected==True).first()
    if doc== None:
        flash("Please select a document first ")
        return redirect(url_for('students.edit_student_documents'))	

    downloaded_file = Ufile.query.filter(Ufile.selected==True).first() 
    if downloaded_file == None:
        flash("Please select a document first ")
        return redirect(url_for('select.file_select'))	

    ##import pdb; pdb.set_trace()
    
    downloaded_file =  send_file(BytesIO(downloaded_file.data), attachment_filename=downloaded_file.name, as_attachment=True)
    return downloaded_file
    #print("Downloaded file: ", downloaded_file)
    #return render_template('edit_document_uploaded_files.html', document=document) 
 
    
    
@doc.route('/download_document_file2/<int:selected_file_id>', methods=['GET', 'POST'])
def download_document_file2(selected_file_id):
    downloded_file = file_select2(selected_file_id)
    ##import pdb; pdb.set_trace()
    return download_document_file()			

##############document's download_files###############	

	
		
