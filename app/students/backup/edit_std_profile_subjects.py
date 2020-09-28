@sbj.route('/edit_std_profile_subjects', methods=['GET', 'POST'])
@login_required
def edit_std_profile_subjects():

    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('index'))
	
    profile = Profile.query.filter(Profile.selected==True).first()
    print("in subjectes_by_profile profile selected is")
    print(profile.title)
    if profile == None:
        flash("Please select an profile first ")
        return redirect(url_for('profile_select'))

    std__subjects = Subject.query.filter(std.profile_id == profile.id)all()
    ##import pdb; pdb.set_trace()
    subjectes = Subject.query.join(Profile.subjects).filter(Profile.id==profile.id)
    
    return render_template('add_subject_to_std_profile.html',
                            student=student,
                            profile=profile,
                            subjectes=all_subjects
							)


@sbj.route('/subject_add', methods=['GET', 'POST'])
def subject_to_std_profile_add():

	student = Student.query.filter(Student.selected==True).first()
	if student == None:
		flash("Please select a student first ")
		return redirect(url_for('index'))
		
	profile = Profile.query.filter(Profile.selected==True).first()

	if profile == None:
		flash("Please select an profile first ")
		return redirect(url_for('profile_select'))
	print(profile.title)      
	#print request

    all_subjects = Subject.query.all()
    std_subjects = profile.subjects
    subjects_not_of_std = list(set(all_subjects).difference(set(std_subjects)))  #subjects_not_of_student = all_subjects-student's subjects

    
	if request.method == 'GET':
		return render_template('subject_not_of_std_profile.html', student=student, profile=profile, subects=subjects_not_of_std)
	###############################################################################		

		   
	#get data from form and insert to subjectgress db
	title = request.form.get('title')
	body = request.form.get('description')

	##import pdb; pdb.set_trace() 	
	author_id = current_user._get_current_object().id
	subject = Subject(title, body, author_id)

	profile.subjects.append(subject)	

	db.session.add(subject)    
	db.session.commit()  
	db.session.refresh(subject)

	url = url_for('subjectes.edit_subjectes')
	return redirect(url)   
	