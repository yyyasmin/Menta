
@prf.route('/get_default_prf/<int:selected_profile_id>/<int:type>', methods=['GET', 'POST'])
def get_default_prf():
       
    prf = Profile.query.filter(Profile.id == selected_profile_id).first()
    
    if prf == None:
        default_prf = Profile.query.filter(Profile.body=='default').first()
        if default_prf == None:
            default_prf = Profile('general', 'default', author_id)	
            db.session.add(default_prf)
            std = get_dummy_student()   # Match new general prf to Humpty Dumpty
            std_gt = attach_gt_to_std(std.id, default_prf.id)
            db.session.commit()
        prf = default_prf
    
    prf = profile_select2(prf.id)  
    
    return prf