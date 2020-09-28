
	
@prf.route('/subject_to_profile_add', methods=['GET', 'POST'])
def subject_to_profile_add(title, body):

    prf = Profile.query.filter(Profile.selected==True).first()
    if prf == None:
        flash("Please select a profile first ")
        return redirect(url_for('profile.edit_profile', from_prf_sort_order=0))		

    if request.method == 'GET':
        return render_template('./backup/subject_to_profile_add.html', profile=prf)
           

    #############################old_prf_scrt pdb.set_trace() 	
    author_id = current_user._get_current_object().id
    ##################old_prf_scrt pdb.set_trace()
    subject = Subject(title, body, author_id)

    db.session.add(subject)  
    if subject not prf.is_parent_of(subject):
        prf.set_parent(subject) 

    ### Add subject to humpty dumpty Demo std ###
    hd = get_dummy_student()
    std_gt = attach_gt_to_std(hd.id, subject.id) 
            
    db.session.commit()  
    url = url_for('profile.edit_profile_subjects' )
    return redirect(url)   

@prf.route('/subject_to_profile_add2/<int:selected_profile_id>', methods=['GET', 'POST'])
def subject_to_profile_add2(selected_profile_id):
	#print(selected_profile_id)
	prf = profile_select2(selected_profile_id)
	return redirect(url_for('profile.subject_to_profile_add'))			
