	
##############studets profiles###############	

@std.route('/edit_students_profile', methods=['GET', 'POST'])
def edit_students_profile():
	#import pdb; pdb.set_trace()
	print("in edit_students_profile")
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('select.student_select'))

	profile = Profile.query.filter(student.profile_id == Profile.id).first()
	if profile:
		return render_template('edit_students_profile.html', student=student,
															 profile=profile)
	else:
		return redirect(url_for('student.profile_to_student_add2', selected_student_id=student.id))
	#import pdb; pdb.set_trace()
	print("In edit_students_profile calling edit_students_profile html ", student.id, profile.id)
	for s in profile.strengthes:
		print("stren:", s.title)
	for w in profile.weaknesses:
		print("weak:", w.title)
	return render_template('edit_students_profile.html', student=student,
														 profile=profile)
	
														  		
@std.route('/edit_students_profile2/<int:selected_student_id>', methods=['GET', 'POST'])
def edit_students_profile2(selected_student_id):
	print("In edit_students_profile2 Request is :", request)
	std = student_select2(selected_student_id)

	prf = Profile.query.filter(std.profile_id == Profile.id).first()
    
	if prf != None:
		prf = profile_select2(prf.id)
	else:f
		return profile_to_student_add()
        
	return edit_students_profile()
 
@std.route('/profile_to_student_add', methods=['GET', 'POST'])
def profile_to_student_add():
    print("In profile_to_student_add")
    user = User.query.get_or_404(current_user._get_current_object().id)
    author_id = user.id
        
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('edit_students'))
    '''
    if request.method == 'GET':
        return render_template('profile_to_student_add.html', student=student)
    '''

    #get data from form and insert to postgress db
    title = request.form.get("profle for std.first_name + std.last_name student")
    body = request.form.get("profle for std.first_name + std.last_name student")

    #import pdb; pdb.set_trace() 	
    prf = Profile(title, body, author_id)	 #Create a new profile 
    prf = profile_select2(prf.id)            # select the new created profile
    student.profile_id = prf.id

       
    db.session.add(profile) 	
    db.session.commit()  
    db.session.refresh(profile)

    print("In profile_to_student_add", student.id, prf.id)

    url = url_for('students.edit_students_profile2', selected_student_id=student.id )
    return redirect(url)   

    @std.route('/profile_to_student_add2/add/<int:selected_student_id>', methods=['GET', 'POST'])
    def profile_to_student_add2(selected_student_id):
        #print("In DDDDDDDDDDDD profile_from_student_delete2")
        std = student_select2(selected_student_id)
        return redirect(url_for('students.profile_to_student_add'))  

	
@std.route('/profile_from_student_delete', methods=['GET', 'POST'])
def profile_from_student_delete():
	#import pdb; pdb.set_trace()
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('select.student_select'))

	profile = Profile.query.filter(Profile.selected==True).first()
	if profile == None:
		flash("Please select a profile first ")
		return redirect(url_for('select.profile_select'))
	
	#print("SSSSSRRRRR IN profile_from_student_delete   deleteing student %s from profile %s :",student.id, profile.id )			

	print("deleteint profile from student %s ", profile.title)		
	db.session.delete(profile)		
	db.session.commit() 
	
	return  redirect(url_for('students.edit_students_profile'))  #no change in students staff profiles
		
@std.route('/profile_from_student_delete2/delete/<int:selected_student_id>/<int:selected_profile_id>', methods=['GET', 'POST'])
def profile_from_student_delete2(selected_student_id, selected_profile_id):
	#print("In DDDDDDDDDDDD profile_from_student_delete2")
	std = student_select2(selected_student_id)
	if selected_profile_id:
		#print(selected_profile_id)
		prf = profile_select2(selected_profile_id)
	return  redirect(url_for('students.profile_from_student_delete'))  

	
	
@std.route('/get_students_profile', methods=['GET', 'POST'])
def get_students_profile():
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('select.student_select'))

	profile = Profile.query.join(Student.pros).filter(Student.id==student.id)	
	return profile

##############studets profiles###############	
