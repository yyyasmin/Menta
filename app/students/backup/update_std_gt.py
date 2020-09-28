    ############## START UPDATE STD GT ################

@std.route('/update_std_gt2', methods=['POST'])
@login_required
def update_std_gt2(txt_type):
    
    #FROM https://stackoverflow.com/questions/43811779/use-many-submit-buttons-in-the-same-form
            
    gt = General_txt.query.filter(General_txt.selected == True).filter(General_txt.type!='profile').first()           
    print(" attaching std.id to gt.id", std.id. gt.id)
    print("")
    
    std_gt = attach_gt_to_std(std.id, gt.id)
        
   
    gt_title_name = "title"+ str(gt.id)
    
    gt_body_name = "body" + str(gt.id)
    
    import pdb; pdb.set_trace()
    print("gt_title_name gt_body_name", gt_title_name, gt_title_name)
    print("form[gt_title_name] form[gt_title_name]", form[gt_title_name], form[gt_title_name])
    print("")
    
    gt.title = form[gt_title_name]
    gt.body = form[gt_body_name]
    
   
    gt.selected = False
        
    db.session.commit() 

    return  redirect(url_for('students.edit_std_profile')) 


@std.route('/update_std_gt2', methods=['GET', 'POST'])
@login_required
def update_std_gt2():
    
    std = Student.query.filter(Student.selected==True).first()
        
    gt_id = int(request.form['str(gt.id)'])    # case of destination 
    
    current_prf = Profile.query.filter(Profile.selected==Trye).first()
    print("current_prf", current_prf)
    
    gt = general_txt_select2(gt_id)
    prf = profile_select2(current_prf.id)
    
    print(" gt", gt, gt.id)
    print("current_prf", current_prf, current_prf.id)
    print("")
    
    import pdb; pdb.set_trace()
    
    return update_std_gt()
    
    ############## START UPDATE STD GT ################
    
