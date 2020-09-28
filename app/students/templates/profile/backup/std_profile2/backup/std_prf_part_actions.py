
    ################## START  ADD GT ################ 

#### POST CASE ####                                                                                     
@prf.route('/std_prf_part_to_profile_add', methods=['GET', 'POST'])
def std_prf_part_to_profile_add(new_gt_type, new_gt_title, new_gt_body):
   

    profile = Profile.query.filter(Profile.selected=='True').first()
    if profile == None:
        flash("Please select a profile to add a part to ")
        return redirect(url_for('profile.edit_profile', from_prf_sort_order=3) )  # Three mens by tag order
    
    '''
    for t in Tag.query.all():
        if profile.is_parent_of(t):
            selected_tag = t
            break

    for st in Sub_tag.query.all():
        if profile.is_parent_of(st):
            selected_sub_tag = st
            break
    '''
    selected_tag = Tag.query.filter(Tag.selected==True).first()
    if selected_tag == None:
        for t in Tag.query.all():
            if t.default==True:
                selected_tag = t 
        
    selected_sub_tag = Sub_tag.query.filter(Sub_tag.selected==True).first()
    if selected_sub_tag == None:
        for st in Sub_tag.query.all():
            if (st.default==True) and (t.is_parent_of(st)):
                selected_tag = t 
        
    #######import pdb; pdb.set_trace()

    print ("In gt_to_profile_add BEFOR VVVVVVVVVVVVVVV validate type, new_gt_title, new_gt_body, new_gt_type, tag  sub_tag : ", 
                                                            type, new_gt_title, new_gt_body, new_gt_type,
                                                            selected_tag.id, selected_sub_tag.id)
    print("")
    print("")
    
              
            
    ### POST Case
    ### FROM https://stackoverflow.com/questions/28209131/wtforms-post-with-selectfield-not-working
    #print ("form.validate_on_submit", form.validate_on_submit)
    
    print("In gt_to_profile_add profile is :", profile, profile.id)
    print("")    
    print("In gt_to_profile_add sub_tag_title is :",  selected_sub_tag,  selected_sub_tag.id)
    print("")  
    print("In gt_to_profile_add tag_title is :", selected_tag, selected_tag.id)
    print("")
    print("In gt_to_profile_add new_gt_title is :", new_gt_title)
    print("")
    print("In gt_to_profile_add new_gt_body is :", new_gt_body)
    print("")
    print("In gt_to_profile_add gt_type is :", new_gt_type)
    
    author_id = current_user._get_current_object().id    
    
    ### CHANgE subject to Subject ###
    new_gt = eval(new_gt_type).query.filter(eval(new_gt_type).title==new_gt_title).filter(eval(new_gt_type).body==new_gt_body).first()            

    if new_gt == None:
        new_gt = eval(new_gt_type)(new_gt_title, new_gt_body, author_id)
        db.session.add(new_gt)
        db.session.commit()
        
    print("new_gt.id  ", new_gt.id)
    
    new_gt = general_txt_select2(new_gt.id)
    
    new_gt.title = new_gt_title
    new_gt.body =  new_gt_body
    
    db.session.add(new_gt)
    db.session.commit()
    
    #new_gt = general_txt_select2(new_gt.id)
    new_gt.set_parent(selected_sub_tag)
    new_gt.set_parent(selected_tag)
    
    db.session.commit()

    std = get_dummy_student()   # Match new gt to Humpty Dumpty
    std_gt = attach_gt_to_std(std.id, new_gt.id) 
    
    ###########################import pdb;; pdb.set_trace()
    profile.set_parent(new_gt)
    
    
    print(" In BEFORE COMMIT the END OF gt_to_profile_add new_gt.gt_type =: " ,new_gt.id,  new_gt.gt_type)
    
    new_gt.selected = False
    db.session.commit()
    
    #DEBUG
    new_gt = General_txt.query.filter(General_txt.id== new_gt.id).first()
    print(" In BEFORE AFTER the END OF gt_to_profile_add new_gt.gt_type =: " ,new_gt.id,  new_gt.gt_type)
    print("")
    #DEBUG
    
    return redirect(url_for('profile.edit_profile', from_prf_sort_order=3) )
          

@std.route('/std_prf_part_to_profile_add2/<int:selected_profile_id>/<int:selected_gt_id>', methods=['GET', 'POST'])
def std_prf_part_to_profile_add2(selected_profile_id, selected_gt_id):

    print("")
    print("")
    print(" IN gt_to_profile_add2:  selected_profile_id, selected_gt_id", selected_profile_id, selected_gt_id)
    gt = general_txt_select2(selected_gt_id)
    prf = profile_select2(prf.id)
        
    author_id = current_user._get_current_object().id    
    
    form = Gt_form()

    ######import pdb; pdb.set_trace()
    
    print("request.form['gt_title'] ",   request.form['gt_title'])
    print("request.form['gt_body'] ",    request.form['gt_body'])
    print("request.form['class_name'] ", request.form['class_name'])
        
    new_gt_title =  request.form['gt_title']
    new_gt_body =  request.form['gt_body']
    new_gt_type =  request.form['class_name']
    
 
    print("  IN END OF gt_to_profile_add2 --- GT: ",new_gt_type, new_gt_title, new_gt_body)
    print("")
    print("")
    return std_prf_part_to_profile_add(new_gt_type, new_gt_title, new_gt_body) 

    ################## END  ADD GT ################ 


    ############### START UPDATE GT ################  
    
@std.route('/std_profile_gt_update', methods=['GET', 'POST'])
def std_profile_gt_update():

    prf = Profile.query.filter(Profile.selected==True).first()
    if prf == None:
        flash("IN std_profile_gt_update Please select a profile part first ")
        return redirect(url_for('profile.std_edit_profile'))		
     
    updated_gt = General_txt.query.filter(General_txt.selected==True).first()    
    if updated_gt == None:
        flash("IN std_profile_gt_update Please part select a profile part to update")
        return redirect(url_for('profile.edit_profile_by_tag') )

    new_prf_part = eval(updated_gt)(request.form['gt_title'], request.form['gt_body'], get_author_id())
    prf.unset_parent(updated_gt)
    prf.set_paren(new_prf_part)
    
    db.session.commit()

    updated_gt.selected = False
    db.session.commit()
    
    return std_edit_profile()
    
#### POST CASE ####                                                                                     
@std.route('/profile_gt_update2/<int:selected_profile_id>/<int:selected_gt_id>', methods=['GET', 'POST'])
def std_profile_gt_update2(selected_profile_id, selected_gt_id):
   
    print(" IN std_profile_gt_update2:  selected_profile_id, selected_gt_id", selected_profile_id, selected_gt_id)
    gt = general_txt_select2(selected_gt_id)
    prf = profile_select2(prf.id)
    
    return redirect(url_for('profile.std_profile_gt_update')) 	
           


    ############## END UPDATE GT ################ 



    ################ END DELETE GT ############## 

@prf.route('/gt_from_profile_delete', methods=['GET', 'POST'])
def gt_from_profile_delete():

    ##########################import pdb; pdb.set_trace()

    profile = Profile.query.filter(Profile.selected==True).first()
    if profile == None:
        flash("IN gt_from_profile_delete Please select a profile first ")
        return redirect(url_for('profile.edit_profile_by_tag'))		

    gts = General_txt.query.filter(General_txt.selected==True).all()
    if gts == None:
        flash("IN gt_from_profile_delete Please select a gt to delete first ")
        return redirect(url_for('select.edit_profile_by_tag'))
           
    for gt in gts:
        if profile.is_parent_of(gt):
                profile.unset_parent(gt)    
                gt.selected = False
                break    
         
    print ("deleted  profile from gt  ",  profile, profile.id,  gt, gt.id  )

    db.session.commit()  

    return redirect(url_for('profile.edit_profile2_by_tag')) 


@prf.route('/gt_from_profile_delete2/<int:selected_profile_id>/<int:selected_gt_id>', methods=['GET', 'POST'])
#Here author is user_id
def gt_from_profile_delete2(selected_profile_id, selected_gt_id):
   
   print(" IN gt_from_profile_delete2:  selected_profile_id, selected_gt_id", selected_profile_id, selected_gt_id)
    gt = general_txt_select2(selected_gt_id)
    prf = profile_select2(prf.id)
    
    return redirect(url_for('profile.gt_from_profile_delete')) 	

    ################## END DELETE GT ################ 
