
##############student's documents###############	

	
@std.route('/edit_student_documents', methods=['GET', 'POST'])
def edit_student_documents():
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('select.edit_destination_students'))	
    import pdb; pdb.set_trace()    
    print("In edit_student_documents student std is::: ", std )
    return render_template('./documents/edit_student_documents.html', std=std) 
                                                                														  		
@std.route('/edit_student_documents2/<int:selected_student_id>', methods=['GET', 'POST'])
def edit_student_documents2(selected_student_id):
    print("In edit_student_documents2 Request is :", request)
    std = student_select2(selected_student_id)
    return redirect(url_for('students.edit_student_documents'))		

	
@std.route('/document_to_student_add', methods=['GET', 'POST'])
def document_to_student_add():
    author_id = current_user._get_current_object().id

    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('select.edit_students'))	

    if request.method == 'GET':
        return render_template('./documents/document_to_std_add.html', std=std)

           
    #get data from form and insert to documentgress db
    title = request.form.get('title')
    body = request.form.get('description')

    document = Document(title, body)

    file_name = request.form.get('file_name')
    uploaded_file = request.files.get('file_name')
    file_name = uploaded_file.filename
    file_data = uploaded_file.read()
    uploaded_file = Ufile(file_name, file_data, author_id)  #find out how to set file_data

    ##########import pdb;pdb.set_trace() 	

    document.files.append(uploaded_file)

    db.session.add(document)    	
    std.documents.append(document)   
    db.session.commit()  
    db.session.refresh(document)
    url = url_for('students.edit_student_documents' )
    return redirect(url)   

@std.route('/document_to_student_add2/<int:selected_student_id>', methods=['GET', 'POST'])
def document_to_student_add2(selected_student_id):
	print("IN document_to_student_add2 std is ::: ", selected_student_id)
	std = student_select2(selected_student_id)
	return redirect(url_for('students.document_to_student_add'))			

	
@std.route('/document_from_student_delete', methods=['GET', 'POST'])
def document_from_student_delete():

    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('select.student_select'))		


    document = Document.query.filter(Document.selected==True).first()
    if document == None:
        flash("Please select a document to delete first ")
        return render_template('edit_student_documents.html', student=student) 
            
    print ("delete selected document is " + document.title + " from slected student " + student.title )

    student.documents.remove(document)
    db.session.commit()  

    return redirect(url_for('students.edit_student_documents')) 

@std.route('/document_from_student_delete2/<int:selected_student_id><int:selected_document_id>', methods=['GET', 'POST'])
#Here author is user_id
def document_from_student_delete2(selected_student_id, selected_document_id):
	std = student_select2(selected_student_id)

	document = document_select2(selected_document_id)
	return redirect(url_for('students.document_from_student_delete')) 	

############## END student's documents###############	