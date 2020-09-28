##############START update std profile ###############	

@std.route('/edit_std_profile', methods=['GET', 'POST'])
@login_required
def edit_std_profile():
	###########################impor pdb;pdb.set_trace()
	#######print("in edit_stds_profile")
	std = Student.query.filter(Student.selected==True).first()
	if std == None:
		flash("Please select a std first ")
		return redirect(url_for('stds.edit_stds'))

	profile = Profile.query.filter(Profile in std.general_txts).first()
	if profile:
		return render_template('./profile/edit_stds_profile.html', std=std, profile=profile)
															 
	else:
		return redirect(url_for('std.profile_to_std_add2', selected_std_id=std.id))

	return render_template('./profile/edit_stds_profile.html', std=std, profile=profile)
														           
	
														  		
@std.route('/<int:selected_std_id>', methods=['GET', 'POST'])
@login_required
def edit_std_profile2(selected_std_id):
	#######print("In edit_stds_profile2 Request is :", request)
	std = std_select2(selected_std_id)

    std_prf = std_general_txt.query.filter(std_general_txt.student_id==srd.id).filter(std_general_txt.general_txt.type=='profile').first()
	prf = std_prf.general_txt
   
	return edit_stds_profile()
 
@std.route('/update_std_profile', methods=['GET', 'POST'])
@login_required
def update_std_profile():
    
    #FROM https://stackoverflow.com/questions/43811779/use-many-submit-buttons-in-the-same-form
        
    std_profile_part = Std_general_txt.query.filter(Std_general_txt.selected==True).first()
    profile_part = General_txt.query.filter(General_txt.selected==True).first()
    
    if std_profile_part == None:
        flash("Please select a std and a txt to match  first ")
        return redirect(url_for('stds.edit_std_destinations'))
		
    print (" std_profile_part:  std_profile_part.id", std_profile_part, std_profile_part.id) 
    print (" profile_part:  profile_part.id", profile_part, profile_part.id) 
    
    std_profile_part.select = False
    profile_part.select = False
    
    return  redirect(url_for('stds.edit_std_destinations')) 

##############END update_std_profile_part ###############	

@std.route('/update_std_profile2', methods=['POST'])
@login_required
def update_std_profile2():
    
    #FROM https://stackoverflow.com/questions/43811779/use-many-submit-buttons-in-the-same-form
    std = Student.query.filter(Student.selected==True).first()

    profile_part_id = int(request.form['profile_txt'])
    import pdb; pdb.set_trace()
    print("profile_part_id profile_part: ", profile_part, profile_part.id)
    profile_part = general_txt_select2(profile_part_id)
    if profile_part == None:
        flash("Please select a profile part to match first ")
        return redirect(url_for('stds.edit_std_profile'))
		
    update_std_profile = attach_gt_to_std(std.id, profile_part_id)
    
    update_std_profile = std_general_txt_select2(std.id, profile_part_id)

    return  redirect(url_for('stds.update_std_profile')) 

##############END update std profile ###############	

