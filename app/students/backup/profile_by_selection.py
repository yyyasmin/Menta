

##############studets subjects###############	
@std.route('/edit_student_subjects', methods=['GET', 'POST'])
@login_required
def edit_student_subjects():
    #######################impor pdb;pdb.set_trace()
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))
                                
    ###########################impor pdb;pdb.set_trace()
    std_age_range = get_student_default_age_range(std.birth_date)
    
    all_tags = Tag.query.all() 
        
    #DEBUG
    std_dst_ids = []
    for st in std.subjects:
        std_dst_ids.append(st.subject_id)
    #print("111111111 std_dst_ids: ", std_dst_ids)
    #######import pdb; pdb.set_trace()
    ########################impor pdb;pdb.set_trace()
    return render_template('./subjects/edit_std_dst_by_tag.html', 
                                                            std = std, 
                                                            tags=all_tags,
                                                            std_dst_ids=std_dst_ids)
                                                               
                                                                
                                                                

																												  		
@std.route('/edit_student_subjects2/edit/<int:selected_student_id>/<int:selected_subject_id>', methods=['GET', 'POST'])
@login_required
def edit_student_subjects2(selected_student_id, selected_subject_id):
	#print("In edit_student_subjects2 Request is :", request)
	std = student_select2(selected_student_id)
	if selected_subject_id != 0:
		dest = subject_select2(selected_subject_id)
	return redirect(url_for('students.edit_student_subjects'))		


@std.route('/update_student_age_range_for_edit_subject/edit/<int:selected_student_id>', methods=['GET', 'POST'])
@login_required
def update_student_age_range_for_edit_subject(selected_student_id):
    #print("In edit_student_subjects2 Request is :", request)
    std = student_select2(selected_student_id)
    student = Student.query.filter(Student.selected==True).first()

    ar_title = request.form.get('selected_age_range')
    ar = Age_range.query.filter(Age_range.title == ar_title).first()
    age_ranges = Age_range.query.all();
    return render_template('./subjects/edit_student_subjects.html', student=student, age_ranges=age_ranges, default_age_range = ar)

@std.route('/update_student_scrt_for_edit_subject/edit/<int:selected_student_id>', methods=['GET', 'POST'])
@login_required
def update_student_scrt_for_edit_subject(selected_student_id):
    #print("In update_student_ scrt_ for_edit_subject Request is :", request)
    std = student_select2(selected_student_id)
    student = Student.query.filter(Student.selected==True).first()

    ar_title = request.form.get('selected_age_range')
    ar = Age_range.query.filter(Age_range.title == ar_title).first()
    age_ranges = Age_range.query.all();
    return render_template('edit_student_subjects.html', student=student, age_ranges=age_ranges, default_age_range = ar)


@std.route('/get_student_default_age_range/<string:birth_date>', methods=['GET', 'POST'])
@login_required
def get_student_default_age_range(birth_date):
    today = date.today()
    age = today.year - birth_date.year
    full_year_passed = (today.month, today.day) < (birth_date.month, birth_date.day)
    if not full_year_passed:
        age -= 1
    age_ranges = Age_range.query.all()
    for ar in age_ranges:
        if ar in range(ar.from_age ,ar.to_age):
            return ar
    if age < 3:
        ar = Age_range.query.filter(Age_range.to_age < 6).first()
    else:  
        ar = Age_range.query.filter(Age_range.from_age > 17).first()
    return ar
            
            
@std.route('/subject_to_student_add', methods=['GET', 'POST'])
@login_required
def subject_to_student_add():
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))		
 
    
    std_dst_ids = []
    for st in std.subjects:
        std_dst_ids.append(st.subject_id)
    
    #######import pdb; pdb.set_trace()
    subjects_of_std_and_dummy = Std_subject.query.filter(Std_subject.student_id==0).filter(Std_subject.subject_id.in_(std_dst_ids)).all()
    all_subjects = Std_subject.query.filter(Std_subject.student_id==0).all()   # Humpty dumpty has id=0 and all subjects 
    subjects_not_of_student = list(set(all_subjects).difference(set(subjects_of_std_and_dummy)))  #subjects_not_of_student = all_subjects-student's subjects

    age_ranges = Age_range.query.all()
    tags = Tag.query.all() 
    ############################impor pdb;pdb.set_trace()
    if request.method == 'GET':
        return render_template('./subjects/edit_subjects_not_of_student.html',
                                                                std=std,
                                                                subjects=subjects_not_of_student, 
                                                                age_ranges=age_ranges,
                                                                tags=tags)

@std.route('/subject_to_student_add2/<int:selected_student_id>', methods=['GET', 'POST'])
@login_required
def subject_to_student_add2(selected_student_id):
	###########################impor pdb;pdb.set_trace()
	std = student_select2(selected_student_id)
	#dest = subject_select2(selected_subject_id)
	return redirect(url_for('students.subject_to_student_add')) 	
	
	
@std.route('/match_subject_to_std_profile', methods=['GET', 'POST'])
@login_required
def match_subject_to_std_profile():
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))		

    sbj = Subject.query.filter(Subject.selected==True).first()	
    if sbj == None:
        flash("Please select a subject to add first ")
        return redirect(url_for('subjectes.edit_subjectes'))

    ############impor pdb;pdb.set_trace()
    print("IN match_subject_to_std_profile", std, sbj)
    #######import pdb; pdb.set_trace()
 		   
	profile.subjects.append(sbj)	

	db.session.add(subject)    
	db.session.commit()  
	db.session.refresh(subject)
    
    sbj.selected=False
	return url = redirect(url_for('subjectes.edit_subjectes'))
			
@std.route('/match_subject_to_std_profile2/<int:selected_subject_id>', methods=['GET', 'POST'])
@login_required
def match_subject_to_std_profile2(selected_subject_id):
    #########################impor pdb;pdb.set_trace()
    dest = subject_select2(selected_subject_id)
    return redirect(url_for('students.match_subject_to_std_profile')) 	


@std.route('/subject_from_std_profile_delete', methods=['GET', 'POST'])
@login_required
def subject_from_std_profile_delete():
	
	std = Student.query.filter(Student.selected==True).first()
	if std == None:
		flash("Please select a student first ")
		return redirect(url_for('subjectes.edit_subjectes'))		

	sbj = Subject.query.filter(Subject.selected==True).first()
	if sbj == None:
		flash("Please select a subject to delete first ")
		return redirect(url_for('subjectes.edit_subjectes'))
			
	#print ("In subject_from_student_delete deleting selected subject is ", subject.title )
	
	student.subjects.remove(subject)
    
	db.session.commit()  

	return redirect(url_for('subjectes.edit_subjectes')) 

@std.route('/subject_from_std_profile_delete2/<int:selected_subject_id>', methods=['GET', 'POST'])
@login_required
def subject_from_std_profile_delete2(selected_subject_id):
	sbj = subject_select2(selected_subject_id)
	return redirect(url_for('students.subject_from_student_delete')) 	

##############studets subjects###############		