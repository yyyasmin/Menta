#***********************************************

    ############## START UPDATE STD GT ################

@std.route('/update_std_gt', methods=['POST'])
@login_required
def update_std_gt():
     
    ###print(" IN update_std_gt:")
    ###print("")
    
    ######################import pdb; #pdb.set_trace()
        
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))
    
   
    std_prf = get_std_gt(std.id, 'Profile')
    ###print(" IN update_std_gt std profile: ", std_prf)
    
    gt = General_txt.query.filter(General_txt.selected == True).filter(General_txt.type!='profile').first()           
    
    std_gt = Std_general_txt.query.filter(Std_general_txt.student_id==std.id).filter(Std_general_txt.general_txt_id==gt.id).first()
    if std_gt == None:    
        ###print(" attaching std.id to gt.id", std.id, gt.id)
        ###print("")
        std_gt = attach_gt_to_std(std.id, gt.id)
     
    ######################import pdb; #pdb.set_trace()
    ###print(" IN update_std_gt setting gt to be a child of orf profile", gt, std_prf)
    ###print("")
    ###print("")
    
    std_prf.set_parent(gt)

    gt.selected = False
        
    db.session.commit() 

    return  redirect(url_for('students.edit_std_profile2', selected_student_id=std.id )) 


@std.route('/update_std_gt2', methods=['GET', 'POST'])
@login_required
def update_std_gt2():
    
    std = Student.query.filter(Student.selected==True).first()
    if std == None:
        flash("Please select a student first ")
        return redirect(url_for('students.edit_students'))
   
    gt_id = int(request.form['save_gt'])    
 
    print("")
    print("")
    print("IN update_std_gt2 -- gt_id:", gt_id)
    print("")
        
    current_prf = Profile.query.filter(Profile.selected==True).first()
        
    ###print("IN update_std_gt2  current_prf", current_prf)
    gt = General_txt.query.filter(General_txt.id==gt_id).first()
    gt = specific_gt_type_select2(gt_id, gt.gt_type)
    
    prf = profile_select2(current_prf.id)
         
    gt_title_name = "title"+ str(gt.id)    
    gt_body_name =  "body" + str(gt.id)
       
    gt.title = request.form[gt_title_name]
    gt.body =  request.form[gt_body_name]
    
    std_gt = attach_gt_to_std(std.id, gt.id)
    prf.set_parent(gt)
    
    db.session.commit()
                   
    return update_std_gt()
    
    ############## START UPDATE STD GT ################
    