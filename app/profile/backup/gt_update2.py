
@prf.route('/gt_update2/<int:selected_profile_id>/<int:type>', methods=['GET', 'POST'])
def gt_update2(selected_profile_id, type):

    print(" IN gt_update2", selected_profile_id, type)
    print("")
    
    form = Gt_form()
    
    
    if not form.validate_on_submit:
        flash("יש לבחור קטגוריה")
        return render_template('dsply_gt_form_for_add.html', form=form)
        
    print(selected_profile_id)
    
    prf = Profile.query.filter(Profile==selected_profile_id).first()
        
    if prf == None:     # get or create a default profile
        prf = Profile.query.filter(Profile.title=='general').first()
        if prf == None:
            prf = Profile('general', 'default', author_id)	
            db.session.add(prf)
            std = get_dummy_student()   # Match new general prf to Humpty Dumpty
            std_gt = attach_gt_to_std(std.id, prf.id) 
            db.session.commit()            

    prf = profile_select2(prf.id)  
    
    
    updated_gt_title = form.gt_title.data
    updated_gt_body =  form.gt_body.data    
    updated_tag =      Tag.query.filter_by(id=form.tag.data).first()
    
    print(" IN dsply_gt_form_for_add2 form: ", new_gt_title, new_gt_body, tag)
    print("")
    print("")
    print("")

    #return redirect(url_for('profile.gt_to_profile_add', type=type, new_gt_title=new_gt_title, new_gt_body=new_gt_body, new_gt_tag=tag))
    return gt_to_profile_add(type, new_gt_title, new_gt_body, tag)
                            			
