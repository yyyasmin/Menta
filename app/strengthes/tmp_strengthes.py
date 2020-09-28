	
##############studets profiles###############	
@std.route('/strengthes_by_profile_show')
@login_required
def strengthes_by_profile_show():
	
    student = Student.query.filter(Student.selected==True).first()
    if student == None:
        flash("Please select a student first ")
        return redirect(url_for('students.index'))
	
	
    #import pdb; pdb.set_trace()
    profile = Profile.query.join(Student.pros).filter(Student.id==student.id)

	return render_template('edit_student_profile.html',
							student=student,
							profile = profile
							)

	
@std.route('/profile_by_student_show2/<int:selected_student_id>', methods=['GET', 'POST'])
def profile_by_student_show2(selected_student_id):
	#print(selected_student_id)
	std = student_select2(selected_student_id)
	return redirect(url_for('student.profile_by_student_show'))
							

@std.route('/edit_student_profile', methods=['GET', 'POST'])
def edit_student_profile():
	
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('select.student_select'))

	profile = Profile.query.join(Student.pros).filter(Student.id==student.id)	
	return render_template('edit_student_profile.html', student=student,
														profile=profile)
		
														  		
@std.route('/edit_student_profile2/edit/<int:selected_student_id>/<int:selected_profile_id>', methods=['GET', 'POST'])
def edit_student_profile2(selected_student_id, selected_profile_id):
	print("In edit_student_profile2 Request is :", request)
	std = student_select2(selected_student_id)
	if selected_profile_id != 0:
		prf = profile_select2(selected_profile_id)
	return edit_student_profile()
 
 
@std.route('/profile_to_student_add', methods=['GET', 'POST'])
def profile_to_student_add():


    user = User.query.get_or_404(current_user.id)
    author_id = user.id
	
    
    profile = Profile.query.filter(Profile.selected==True).first()
    if profile == None:
        flash("Please select a profile first ")
        return redirect(url_for('students.index'))
        
    student = Student.query.filter(Student.selected==True).first()
    
    if student == None:
        flash("Please select an student first ")
        return redirect(url_for('select.student_select'))
    #print request
    
    if request.method == 'GET':
        return render_template('student.profile_to_student_add.html', action=action)
           
    #get data from form and insert to postgress db
	title = request.form.get('title')
    body = request.form.get('body')
	
    #import pdb; pdb.set_trace() 	
    profile = Profile(title, body)	
	
    student.profile.append(profile)	
	   
    db.session.add(profile)    
    db.session.commit()  
    db.session.refresh(profile)
    # test insert res
    url = url_for('student.edit_student_profile')
    return redirect(url)   
	
	
	
		
	
@std.route('/profile_to_student_add2/add/<int:selected_profile_id>/<int:selected_student_id>', methods=['GET', 'POST'])
def profile_to_student_add2(selected_profile_id, selected_student_id):
	print(selected_student_id)
	student_select2(selected_student_id)
	print(selected_profile_id)
	profile_select2(selected_profile_id)
	return profile_to_student_add()
	

	
@std.route('/student_from_profile_delete', methods=['GET', 'POST'])
def student_from_profile_delete():
	import pdb; pdb.set_trace()
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('select.student_select'))

	profile = Profile.query.filter(Profile.selected==True).first()
	if profile == None:
		flash("Please select a profile first ")
		return redirect(url_for('select.profile_select'))
		
	#print("SSSSSRRRRR IN student_from_profile_delete   deleteing student %s from profile %s :",student.id, profile.id )			

	role = Role.query.filter(Role.student_id == student.id).filter(Role.profile_id==profile.id).first()   #update role
	if role:
		print ("DEleting OLD ROLE ", role.title)
		role.title = "No Role"

   
	db.session.commit() 
	db.session.refresh(student)
	db.session.refresh(profile)
	
	#DEBUG
	if role:
		role = Role.query.filter(Role.student_id == student.id).filter(Role.profile_id==profile.id).first()   #update role
		print ("NEW ROLE IS ", role.title)
	#DEBUG
	
	return  redirect(url_for('students.edit_student_profiles'))  #no change in students staff profiles
		
@std.route('/student_from_profile_delete2/delete/<int:selected_profile_id>/<int:selected_student_id>', methods=['GET', 'POST'])
def student_from_profile_delete2(selected_profile_id, selected_student_id):
	#print("In DDDDDDDDDDDD student_from_profile_delete2")
	std = student_select2(selected_student_id)
	if selected_profile_id:
		#print(selected_profile_id)
		tchr = profile_select2(selected_profile_id)
	return  redirect(url_for('students.student_from_profile_delete'))  

	
	
@std.route('/get_student_profiles', methods=['GET', 'POST'])
def get_student_profiles():
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('select.student_select'))
	
	#DEBUG
	#import pdb; pdb.set_trace()	
	all_profiles = Profile.query.all()
	'''
	for t in all_profiles:
		#print("TEacher students list :", t.id, t.students)
	'''
	student_staff_profiles = Profile.query.join(Role).filter(Role.student_id==student.id).filter(Role.profile_id==Profile.id).all()

	return student_staff_profiles



@std.route('/get_profiles_not_of_student', methods=['GET', 'POST'])
def get_profiles_not_of_student():
	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('select.student_select'))
	
	#DEBUG
	#import pdb; pdb.set_trace()	
	all_profiles = Profile.query.all()
	'''
	for t in all_profiles:
		#print("TEacher students list :", t.id, t.students)
	'''
	student_staff_profiles = Profile.query.join(Role).filter(Role.student_id==student.id).filter(Role.profile_id==Profile.id).all()
	
	profiles_with_no_students = Profile.query.filter(~Profile.students.any()).all()
	
	profiles_not_in_staff = list(set(all_profiles).difference(set(student_staff_profiles)))  #profiles_not_in_staff = all_profiles-student_staff_profiles
	
	profiles_not_in_staff.extend(profiles_with_no_students)

	#import pdb; pdb.set_trace()
	#DEBUG

	return profiles_not_in_staff
##############studets profiles###############	








