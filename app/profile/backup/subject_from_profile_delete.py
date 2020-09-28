	
@prf.route('/subject_from_profile_delete', methods=['GET', 'POST'])
def subject_from_profile_delete():
	
	profile = Profile.query.filter(Profile.selected==True).first()
	if profile == None:
		flash("Please select a profile first ")
		return redirect(url_for('profiles.edit_profiles', from_prf_sort_order=0))		


	subject = Subject.query.filter(Subject.selected==True).first()
	if subject == None:
		flash("Please select a subject to delete first ")
		return redirect(url_for('select.edit_profile_subjects'))
			
	#print ("delete selected subject is " + subject.title + " from slected profile " + profile.title )
    
    subject.selected = False
    
    profile.unset_parent(subject)
	db.session.commit()  

	return redirect(url_for('profiles.edit_profiles_subjects')) 

@prf.route('/subject_from_profile_delete2/<int:selected_profile_id><int:selected_subject_id>', methods=['GET', 'POST'])
#Here author is user_id
def subject_from_profile_delete2(selected_profile_id, selected_subject_id):

	prf = profile_select2(selected_profile_id)
	sbj = subject_select2(selected_subject_id)
	return redirect(url_for('profiles.subject_from_profile_delete')) 	

