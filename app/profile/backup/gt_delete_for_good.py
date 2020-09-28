
@prf.route('/gt_from_profile_delete_for_good', methods=['GET', 'POST'])
def gt_from_profile_delete_for_good():
	
    profile = Profile.query.filter(Profile.selected==True).first()
    if profile == None:
        flash("Please select a profile first ")
        return redirect(url_for('profile.edit_profile_by_tag', from_prf_sort_order=0))		

    gt = General_txt.query.filter(General_txt.selected==True).first()
    if gt == None:
        flash("Please select a gt to delete first ")
        return redirect(url_for('select.edit_profile_by_tag'))
            
    #print ("delete selected gt is " + gt.title + " from slected profile " + profile.title )

    for c in gener

    profile.unset_parent(gt)
    db.session.commit()  

    return redirect(url_for('profile.edit_profile_by_tag_gts')) 

@prf.route('/gt_from_profile_delete_for_good2/<int:selected_profile_id>/<int:selected_gt_id>', methods=['GET', 'POST'])
#Here author is user_id
def gt_from_profile_delete_for_good2(selected_profile_id, selected_gt_id):
    print(" IN gt_from_profile_delete_for_good2", selected_gt_id)
    prf = Profile.query.filter(Profile.body=='default').first()
    prf = profile_select2(prf.id)
    gt = general_txt_select2(selected_gt_id)
    return redirect(url_for('profile.gt_from_profile_delete_for_good')) 	

