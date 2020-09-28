
##############studets profile wkns


@std.route('/edit_std_profile_weaknesss', methods=['GET', 'POST'])
@login_required
def edit_std_profile_weaknesss():

    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('index'))
	
    profile = Profile.query.filter(Profile.selected==True).first()
    print("in weaknesses_by_profile profile selected is")
    print(profile.title)
    if profile == None:
        flash("Please select an profile first ")
        return redirect(url_for('profile_select'))

    std_weaknesss = Weakness.query.filter(std.profile_id == profile.id).all()
    ###import pdb; pdb.set_trace()
    weaknesses = Weakness.query.join(Profile.weaknesss).filter(Profile.id==profile.id)
    
    return render_template('./profile/edit_students_profile.html',
                            student=std,
                            profile=profile,
                            weaknesses=std_weaknesss
							)


	
@std.route('/match_weakness_to_std_profile', methods=['GET', 'POST'])
@login_required
def match_weakness_to_std_profile():
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))		

    wkns = Weakness.query.filter(Weakness.selected==True).first()	
    if wkns == None:
        flash("Please select a weakness to add first ")
        return redirect(url_for('weaknesses.edit_weaknesses'))

    profile = Profile.query.filter(Profile.selected==True).first()	
    if profile == None:
        flash("Please select a profile  first ")
        return redirect(url_for('weaknesses.edit_studnets'))

    ############impor pdb;pdb.set_trace()
    print("IN match_weakness_to_std_profile", profile, std, wkns)
    ########import pdb; pdb.set_trace()
           
    profile.weaknesss.append(wkns)	

    db.session.add(wkns)    
    db.session.commit()  
    db.session.refresh(wkns)

    wkns.selected=False
    return redirect(url_for('students.edit_students_profile'))
			
@std.route('/match_weakness_to_std_profile2/<int:selected_weakness_id>', methods=['GET', 'POST'])
@login_required
def match_weakness_to_std_profile2(selected_weakness_id):
    #import pdb;pdb.set_trace()
    wkns = weakness_select2(selected_weakness_id)
    return redirect(url_for('students.match_weakness_to_std_profile')) 	

            
@std.route('/weakness_to_std_profile_add', methods=['GET', 'POST'])
@login_required
def weakness_to_std_profile_add():

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
    all_weaknesss = Weakness.query.all()
    weaknesss_not_of_student = list(set(all_weaknesss).difference(set(profile.weaknesss)))  #weaknesss_not_of_student = all_weaknesss-student's weaknesss

    ############################impor pdb;pdb.set_trace()
    if request.method == 'GET':
        return render_template('./profile/edit_weaknesss_not_of_std2.html',
                                                                student=std,
                                                                profile=profile,
                                                                weaknesss=weaknesss_not_of_student) 
                                                                

@std.route('/weakness_to_std_profile_add2/<int:selected_student_id>', methods=['GET', 'POST'])
@login_required
def weakness_to_std_profile_add2(selected_student_id):
	###########################impor pdb;pdb.set_trace()
	std = student_select2(selected_student_id)
	#dest = weakness_select2(selected_weakness_id)
	return redirect(url_for('students.weakness_to_std_profile_add')) 	
	
	
@std.route('/weakness_from_std_profile_delete', methods=['GET', 'POST'])
@login_required
def weakness_from_std_profile_delete():
	
    profile = Profile.query.filter(Profile.selected==True).first()	
    if profile == None:
        flash("Please select a profile  first ")
        return redirect(url_for('weaknesses.edit_studnets'))

    wkns = Weakness.query.filter(Weakness.selected==True).first()
    if wkns == None:
        flash("Please select a weakness to delete first ")
        return redirect(url_for('weaknesses.edit_weaknesses'))
            
    print ("DDDDDDDDDDDDDD In weakness_from_student_delete deleting  profile weakness ", profile, wkns )

    profile.weaknesss.remove(wkns)

    db.session.commit()  

    return redirect(url_for('students.edit_students_profile')) 

@std.route('/weakness_from_std_profile_delete2/<int:selected_weakness_id>', methods=['GET', 'POST'])
@login_required
def weakness_from_std_profile_delete2(selected_weakness_id):
	wkns = weakness_select2(selected_weakness_id)
	return redirect(url_for('students.weakness_from_std_profile_delete')) 	

##############studets profile wkns


##############studets profiles###############	
