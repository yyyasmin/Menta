
##############student's resources###############	

@student.route('/edit_student_resources', methods=['GET', 'POST'])
def edit_student_resources():

	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('select.edit_destination_students'))	
        
	print("In edit_student_resources student for show tree: " )
	return render_template('edit_student_resources.html', student=student) 
																
														  		
@student.route('/edit_student_resources2/<int:selected_student_id>', methods=['GET', 'POST'])
def edit_student_resources2(selected_student_id):
	print("In edit_student_resources2 Request is :", request)
	std = student_select2(selected_student_id)
	return redirect(url_for('students.edit_student_resources'))		

	
@student.route('/resource_to_student_add', methods=['GET', 'POST'])
def resource_to_student_add():
    author_id = current_user._get_current_object().id

    student = Student.query.filter(Student.selected==True).first()
    if student == None:
        flash("Please select a student first ")
        return redirect(url_for('select.edit
        _students'))	

    if request.method == 'GET':
        return render_template('resource_to_student_add.html', student=student)

           
    #get data from form and insert to resourcegress db
    title = request.form.get('title')
    body = request.form.get('description')

    resource = Resource(title, body)

    file_name = request.form.get('file_name')
    uploaded_file = request.files.get('file_name')
    file_name = uploaded_file.filename
    file_data = uploaded_file.read()
    uploaded_file = Ufile(file_name, file_data, author_id)  #find out how to set file_data

    ##########import pdb;pdb.set_trace() 	

    resource.files.append(uploaded_file)

    db.session.add(resource)    	
    student.resources.append(resource)   
    db.session.commit()  
    db.session.refresh(resource)
    url = url_for('students.edit_student_resources' )
    return redirect(url)   

@student.route('/resource_to_student_add2/<int:selected_student_id>', methods=['GET', 'POST'])
def resource_to_student_add2(selected_student_id):
	print(selected_student_id)
	student = student_select2(selected_student_id)
	return redirect(url_for('students.resource_to_student_add'))			

	
@student.route('/resource_from_student_delete', methods=['GET', 'POST'])
def resource_from_student_delete():

    student = Student.query.filter(Student.selected==True).first()
    if student == None:
        flash("Please select a student first ")
        return redirect(url_for('select.student_select'))		


    resource = Resource.query.filter(Resource.selected==True).first()
    if resource == None:
        flash("Please select a resource to delete first ")
        return render_template('edit_student_resources.html', student=student) 
            
    print ("delete selected resource is " + resource.title + " from slected student " + student.title )

    student.resources.remove(resource)
    db.session.commit()  

    return redirect(url_for('students.edit_student_resources')) 

@student.route('/resource_from_student_delete2/<int:selected_student_id><int:selected_resource_id>', methods=['GET', 'POST'])
#Here author is user_id
def resource_from_student_delete2(selected_student_id, selected_resource_id):
	student = student_select2(selected_student_id)

	resource = resource_select2(selected_resource_id)
	return redirect(url_for('students.resource_from_student_delete')) 	

############## END student's resources###############	

