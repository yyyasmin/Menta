
##############studets profile strn


@std.route('/edit_std_profile_strengthes', methods=['GET', 'POST'])
@login_required
def edit_std_profile_strengthes():

    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('index'))
	
    profile = Profile.query.filter(Profile.selected==True).first()
    print("in strengthes_by_profile profile selected is")
    print(profile.title)
    if profile == None:
        flash("Please select an profile first ")
        return redirect(url_for('profile_select'))

    std_strengthes = Weakness.query.filter(std.profile_id == profile.id).all()
    ###import pdb; pdb.set_trace()
    strengthes = Weakness.query.join(Profile.strengthes).filter(Profile.id==profile.id)
    
    return render_template('./profile/edit_students_profile.html',
                            student=std,
                            profile=profile,
                            strengthes=std_strengthes
							)


	
@std.route('/match_strength_to_std_profile', methods=['GET', 'POST'])
@login_required
def match_strength_to_std_profile():
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))		

    strn = Weakness.query.filter(Weakness.selected==True).first()	
    if strn == None:
        flash("Please select a strength to add first ")
        return redirect(url_for('strengthes.edit_strengthes'))

    profile = Profile.query.filter(Profile.selected==True).first()	
    if profile == None:
        flash("Please select a profile  first ")
        return redirect(url_for('strengthes.edit_studnets'))

    ############impor pdb;pdb.set_trace()
    print("IN match_strength_to_std_profile", profile, std, strn)
    ########import pdb; pdb.set_trace()
           
    profile.strengthes.append(strn)	

    db.session.add(strn)    
    db.session.commit()  
    db.session.refresh(strn)

    strn.selected=False
    return redirect(url_for('students.edit_students_profile'))
			
@std.route('/match_strength_to_std_profile2/<int:selected_strength_id>', methods=['GET', 'POST'])
@login_required
def match_strength_to_std_profile2(selected_strength_id):
    #import pdb;pdb.set_trace()
    strn = strength_select2(selected_strength_id)
    return redirect(url_for('students.match_strength_to_std_profile')) 	

            
@std.route('/strength_to_std_profile_add', methods=['GET', 'POST'])
@login_required
def strength_to_std_profile_add():

    #import pdb; pdb.set_trace()
    
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))		
 
    profile = Profile.query.filter(Profile.selected==True).first()
    if profile == None:
        flash("Please select a profile first ")
        return redirect(url_for('students.edit_students'))		

    #import pdb; pdb.set_trace()
    all_strengthes = Weakness.query.all()
    strengthes_not_of_student = list(set(all_strengthes).difference(set(profile.strengthes)))  #strengthes_not_of_student = all_strengthes-student's strengthes

    ############################impor pdb;pdb.set_trace()
    if request.method == 'GET':
        return render_template('./profile/edit_strengthes_not_of_std2.html',
                                                                student=std,
                                                                profile=profile,
                                                                strengthes=strengthes_not_of_student) 
                                                                

@std.route('/strength_to_std_profile_add2/<int:selected_student_id>', methods=['GET', 'POST'])
@login_required
def strength_to_std_profile_add2(selected_student_id):
	###########################impor pdb;pdb.set_trace()
	std = student_select2(selected_student_id)
	#dest = strength_select2(selected_strength_id)
	return redirect(url_for('students.strength_to_std_profile_add')) 	
	
	
@std.route('/strength_from_std_profile_delete', methods=['GET', 'POST'])
@login_required
def strength_from_std_profile_delete():
	
    profile = Profile.query.filter(Profile.selected==True).first()	
    if profile == None:
        flash("Please select a profile  first ")
        return redirect(url_for('strengthes.edit_studnets'))

    strn = Weakness.query.filter(Weakness.selected==True).first()
    if strn == None:
        flash("Please select a strength to delete first ")
        return redirect(url_for('strengthes.edit_strengthes'))
            
    print ("DDDDDDDDDDDDDD In strength_from_student_delete deleting  profile strength ", profile, strn )

    profile.strengthes.remove(strn)

    db.session.commit()  

    return redirect(url_for('students.edit_students_profile')) 

@std.route('/strength_from_std_profile_delete2/<int:selected_strength_id>', methods=['GET', 'POST'])
@login_required
def strength_from_std_profile_delete2(selected_strength_id):
	strn = strength_select2(selected_strength_id)
	return redirect(url_for('students.strength_from_std_profile_delete')) 	

##############studets profile strn
